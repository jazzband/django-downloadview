import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django_downloadview.middlewares import (ProxiedDownloadMiddleware,
                                             NoRedirectionMatch)
from django_downloadview.nginx.response import XAccelRedirectResponse


class XAccelRedirectMiddleware(ProxiedDownloadMiddleware):
    """Configurable middleware, for use in decorators or in global middlewares.

    Standard Django middlewares are configured globally via settings. Instances
    of this class are to be configured individually. It makes it possible to
    use this class as the factory in
    :py:class:`django_downloadview.decorators.DownloadDecorator`.

    """
    def __init__(self, source_dir=None, source_url=None, destination_url=None,
                 expires=None, with_buffering=None, limit_rate=None,
                 media_root=None, media_url=None):
        """Constructor."""
        if media_url is not None:
            warnings.warn("%s ``media_url`` is deprecated. Use "
                          "``destination_url`` instead."
                          % self.__class__.__name__,
                          DeprecationWarning)
            if destination_url is None:
                destination_url = media_url
            else:
                destination_url = destination_url
        else:
            destination_url = destination_url
        if media_root is not None:
            warnings.warn("%s ``media_root`` is deprecated. Use "
                          "``source_dir`` instead." % self.__class__.__name__,
                          DeprecationWarning)
            if source_dir is None:
                source_dir = media_root
            else:
                source_dir = source_dir
        else:
            source_dir = source_dir
        super(XAccelRedirectMiddleware, self).__init__(source_dir,
                                                       source_url,
                                                       destination_url)
        self.expires = expires
        self.with_buffering = with_buffering
        self.limit_rate = limit_rate

    def process_download_response(self, request, response):
        """Replace DownloadResponse instances by NginxDownloadResponse ones."""
        try:
            redirect_url = self.get_redirect_url(response)
        except NoRedirectionMatch:
            return response
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
                                      limit_rate=self.limit_rate,
                                      attachment=response.attachment)


class SingleXAccelRedirectMiddleware(XAccelRedirectMiddleware):
    """Apply X-Accel-Redirect globally, via Django settings.

    Available settings are:

    NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_URL:
      The string at the beginning of URLs to replace with
      ``NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL``.
      If ``None``, then URLs aren't captured.
      Defaults to ``settings.MEDIA_URL``.

    NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR:
      The string at the beginning of filenames (path) to replace with
      ``NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL``.
      If ``None``, then filenames aren't captured.
      Defaults to ``settings.MEDIA_ROOT``.

    NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL:
      The base URL where requests are proxied to.
      If ``None`` an ImproperlyConfigured exception is raised.

    .. note::

       The following settings are deprecated since version 1.1.
       URLs can be used as redirection source since 1.1, and then "MEDIA_ROOT"
       and "MEDIA_URL" became too confuse.

       NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT:
         Replaced by ``NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR``.

       NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL:
         Replaced by ``NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL``.

    """
    def __init__(self):
        """Use Django settings as configuration."""
        if settings.NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL is None:
            raise ImproperlyConfigured(
                'settings.NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL is '
                'required by %s middleware' % self.__class__.__name__)
        super(SingleXAccelRedirectMiddleware, self).__init__(
            source_dir=settings.NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR,
            source_url=settings.NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_URL,
            destination_url=settings.NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL,
            expires=settings.NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES,
            with_buffering=settings.NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING,
            limit_rate=settings.NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE)
