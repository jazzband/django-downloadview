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
        basename = basename or redirect_url.split('/')[-1]
        self['Content-Disposition'] = 'attachment; filename=%s' % basename
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


class BaseXAccelRedirectMiddleware(BaseDownloadMiddleware):
    """Looks like a middleware, but it is configurable.

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
