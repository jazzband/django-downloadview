"""Optimizations for Nginx.

See also `Nginx X-accel documentation <http://wiki.nginx.org/X-accel>`_ and
:doc:`narrative documentation about Nginx optimizations
</optimizations/nginx>`.

"""
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from django_downloadview.decorators import DownloadDecorator
from django_downloadview.middlewares import BaseDownloadMiddleware
from django_downloadview.utils import content_type_to_charset


#: Default value for X-Accel-Buffering header.
#: Also default value for
#: ``settings.NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Buffering
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#: 
#: If set to ``False``, Nginx buffering is disabled.
#: If set to ``True``, Nginx buffering is enabled.
DEFAULT_WITH_BUFFERING = None
if not hasattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING'):
    setattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING',
            DEFAULT_WITH_BUFFERING)


#: Default value for X-Accel-Limit-Rate header.
#: Also default value for ``settings.NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Rate
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#: 
#: If set to ``False``, Nginx limit rate is disabled.
#: Else, it indicates the limit rate in bytes.
DEFAULT_LIMIT_RATE = None
if not hasattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE'):
    setattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE', DEFAULT_LIMIT_RATE)


#: Default value for X-Accel-Limit-Expires header.
#: Also default value for ``settings.NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Expires
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#: 
#: If set to ``False``, Nginx buffering is disabled.
#: Else, it indicates the expiration delay, in seconds.
DEFAULT_EXPIRES = None
if not hasattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES'):
    setattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES', DEFAULT_EXPIRES)


class XAccelRedirectResponse(HttpResponse):
    """Http response that delegates serving file to Nginx."""
    def __init__(self, redirect_url, content_type, basename=None, expires=None,
                 with_buffering=None, limit_rate=None):
        """Return a HttpResponse with headers for Nginx X-Accel-Redirect."""
        super(XAccelRedirectResponse, self).__init__(content_type=content_type)
        self.basename = basename or redirect_url.split('/')[-1]
        self['Content-Disposition'] = 'attachment; filename=%s' % self.basename
        self['X-Accel-Redirect'] = redirect_url
        self['X-Accel-Charset'] = content_type_to_charset(content_type)
        if with_buffering is not None:
            self['X-Accel-Buffering'] = with_buffering and 'yes' or 'no'
        if expires:
            expire_seconds = timedelta(expires - datetime.now()).seconds
            self['X-Accel-Expires'] = expire_seconds
        elif expires is not None:  # We explicitely want it off.
            self['X-Accel-Expires'] = 'off'
        if limit_rate is not None:
            self['X-Accel-Limit-Rate'] = limit_rate and '%d' % limit_rate \
                                                    or 'off'


class XAccelRedirectValidator(object):
    """Utility class to validate XAccelRedirectResponse instances.

    See also :py:func:`assert_x_accel_redirect` shortcut function.

    """
    def __call__(self, test_case, response, **assertions):
        """Assert that ``response`` is a valid X-Accel-Redirect response.

        Optional ``assertions`` dictionary can be used to check additional
	items:
    
        * ``basename``: the basename of the file in the response.
    
        * ``content_type``: the value of "Content-Type" header.
    
        * ``redirect_url``: the value of "X-Accel-Redirect" header.
    
        * ``charset``: the value of ``X-Accel-Charset`` header.
    
        * ``with_buffering``: the value of ``X-Accel-Buffering`` header.
          If ``False``, then makes sure that the header disables buffering.
          If ``None``, then makes sure that the header is not set.
    
        * ``expires``: the value of ``X-Accel-Expires`` header.
          If ``False``, then makes sure that the header disables expiration.
          If ``None``, then makes sure that the header is not set.
    
        * ``limit_rate``: the value of ``X-Accel-Limit-Rate`` header.
          If ``False``, then makes sure that the header disables limit rate.
          If ``None``, then makes sure that the header is not set.

        """
	self.assert_x_accel_redirect_response(test_case, response)
        for key, value in assertions.iteritems():
            assert_func = getattr(self, 'assert_%s' % key)
	    assert_func(test_case, response, value)

    def assert_x_accel_redirect_response(self, test_case, response):
        test_case.assertTrue(isinstance(response, XAccelRedirectResponse))

    def assert_basename(self, test_case, response, value):
        test_case.assertEqual(response.basename, value)

    def assert_content_type(self, test_case, response, value):
        test_case.assertEqual(response['Content-Type'], value)

    def assert_redirect_url(self, test_case, response, value):
        test_case.assertEqual(response['X-Accel-Redirect'], value)

    def assert_charset(self, test_case, response, value):
        test_case.assertEqual(response['X-Accel-Charset'], value)

    def assert_with_buffering(self, test_case, response, value):
        header = 'X-Accel-Buffering'
        if value is None:
            test_case.assertFalse(header in response)
        elif value:
            test_case.assertEqual(header, 'yes')
        else:
            test_case.assertEqual(header, 'no')

    def assert_expires(self, test_case, response, value):
        header = 'X-Accel-Expires'
        if value is None:
            test_case.assertFalse(header in response)
        elif not value:
            test_case.assertEqual(header, 'off')
        else:
            test_case.assertEqual(header, value)

    def assert_limit_rate(self, test_case, response, value):
        header = 'X-Accel-Limit-Rate'
        if value is None:
            test_case.assertFalse(header in response)
        elif not value:
            test_case.assertEqual(header, 'off')
        else:
            test_case.assertEqual(header, value)


def assert_x_accel_redirect(test_case, response, **assertions):
    """Make ``test_case`` assert that ``response`` is a XAccelRedirectResponse.

    Optional ``assertions`` dictionary can be used to check additional items:

    * ``basename``: the basename of the file in the response.

    * ``content_type``: the value of "Content-Type" header.

    * ``redirect_url``: the value of "X-Accel-Redirect" header.

    * ``charset``: the value of ``X-Accel-Charset`` header.

    * ``with_buffering``: the value of ``X-Accel-Buffering`` header.
      If ``False``, then makes sure that the header disables buffering.
      If ``None``, then makes sure that the header is not set.

    * ``expires``: the value of ``X-Accel-Expires`` header.
      If ``False``, then makes sure that the header disables expiration.
      If ``None``, then makes sure that the header is not set.

    * ``limit_rate``: the value of ``X-Accel-Limit-Rate`` header.
      If ``False``, then makes sure that the header disables limit rate.
      If ``None``, then makes sure that the header is not set.

    """
    validator = XAccelRedirectValidator()
    return validator(test_case, response, **assertions)


class BaseXAccelRedirectMiddleware(BaseDownloadMiddleware):
    """Configurable middleware, for use in decorators or in global middlewares.

    Standard Django middlewares are configured globally via settings. Instances
    of this class are to be configured individually. It makes it possible to
    use this class as the factory in
    :py:class:`django_downloadview.decorators.DownloadDecorator`.

    """
    def __init__(self, media_root, media_url, expires=None,
                 with_buffering=None, limit_rate=None):
        """Constructor."""
        self.media_root = media_root
        self.media_url = media_url
        self.expires = expires
        self.with_buffering = with_buffering
        self.limit_rate = limit_rate

    def get_redirect_url(self, response):
        """Return redirect URL for file wrapped into response."""
        absolute_filename = response.filename
        relative_filename = absolute_filename[len(self.media_root):]
        return '/'.join((self.media_url.rstrip('/'),
                         relative_filename.strip('/')))

    def process_download_response(self, request, response):
        """Replace DownloadResponse instances by NginxDownloadResponse ones."""
        redirect_url = self.get_redirect_url(response)
        if self.expires:
            expires = self.expires
        else:
            try:
                expires = response.expires
            except AttributeError:
                expires = None
        return XAccelRedirectResponse(redirect_url=redirect_url,
                                      content_type=response['Content-Type'],
                                      basename=response.basename,
                                      expires=expires,
                                      with_buffering=self.with_buffering,
                                      limit_rate=self.limit_rate)


class XAccelRedirectMiddleware(BaseXAccelRedirectMiddleware):
    """Apply X-Accel-Redirect globally, via Django settings."""
    def __init__(self):
        """Use Django settings as configuration."""
        try:
            media_root = settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT
        except AttributeError:
            raise ImproperlyConfigured(
                'settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT is required by '
                '%s middleware' % self.__class__.name)
        try:
            media_url = settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL
        except AttributeError:
            raise ImproperlyConfigured(
                'settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL is required by '
                '%s middleware' % self.__class__.name)
        super(XAccelRedirectMiddleware, self).__init__(
            media_root,
            media_url,
            expires=settings.NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES,
            with_buffering=settings.NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING,
            limit_rate=settings.NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE)


#: Apply BaseXAccelRedirectMiddleware to ``view_func`` response.
#:
#: Proxies additional arguments (``*args``, ``**kwargs``) to
#: :py:class:`BaseXAccelRedirectMiddleware` constructor (``expires``,
#: ``with_buffering``, and ``limit_rate``).
x_accel_redirect = DownloadDecorator(BaseXAccelRedirectMiddleware)
