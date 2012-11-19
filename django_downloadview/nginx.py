"""Let Nginx serve files for increased performance.

See `Nginx X-accel documentation <http://wiki.nginx.org/X-accel>`_.

"""
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse

from django_downloadview.middlewares import BaseDownloadMiddleware
from django_downloadview.decorators import DownloadDecorator


#: Default value for X-Accel-Buffering header.
DEFAULT_BUFFERING = None
if not hasattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_BUFFERING'):
    setattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_BUFFERING', DEFAULT_BUFFERING)


#: Default value for X-Accel-Limit-Rate header.
DEFAULT_LIMIT_RATE = None
if not hasattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE'):
    setattr(settings, 'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT', DEFAULT_LIMIT_RATE)


def content_type_to_charset(content_type):
    return 'utf-8'


class XAccelRedirectResponse(HttpResponse):
    """Http response that delegate serving file to Nginx."""
    def __init__(self, url, content_type, basename=None, expires=None,
                 with_buffering=None, limit_rate=None):
        """Return a HttpResponse with headers for Nginx X-Accel-Redirect."""
        super(XAccelRedirectResponse, self).__init__(content_type=content_type)
        basename = basename or url.split('/')[-1]
        self['Content-Disposition'] = 'attachment; filename=%s' % basename
        self['X-Accel-Redirect'] = url
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
    """Looks like a middleware, but configurable."""
    def __init__(self, expires=None, with_buffering=None, limit_rate=None):
        """Constructor."""
        self.expires = expires
        self.with_buffering = with_buffering
        self.limit_rate = limit_rate

    def file_to_url(response):
        return response.filename

    def process_download_response(self, request, response):
        """Replace DownloadResponse instances by NginxDownloadResponse ones."""
        url = self.file_to_url(response)
        if self.expires:
            expires = self.expires
        else:
            try:
                expires = response.expires
            except AttributeError:
                expires = None
        return XAccelRedirectResponse(url=url,
                                      content_type=response.content_type,
                                      basename=response.basename,
                                      expires=expires,
                                      with_buffering=self.with_buffering,
                                      limit_rate=self.limit_rate)


class XAccelRedirectMiddleware():
    """Apply X-Accel-Redirect globally.

    XAccelRedirectResponseHandler with django settings.

    """
    def __init__(self):
        """Use Django settings as configuration."""
        super(XAccelRedirectMiddleware, self).__init__(
            expires=settings.NGINX_DOWNLOAD_MIDDLEWARE_EXPIRESS,
            with_buffering=settings.NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING,
            limit_rate=settings.NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE)


#: Apply BaseXAccelRedirectMiddleware to ``view_func`` response.
#:
#: Proxies additional arguments (``*args``, ``**kwargs``) to
#: :py:meth:`django_downloadview.nginx.BaseXAccelRedirectMiddleware.__init__`:
#: ``expires``, ``with_buffering``, and ``limit_rate``.
x_accel_redirect = DownloadDecorator(BaseXAccelRedirectMiddleware)
