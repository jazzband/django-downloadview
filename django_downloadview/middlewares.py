# -*- coding: utf-8 -*-
"""Base material for download middlewares.

Download middlewares capture :py:class:`django_downloadview.DownloadResponse`
responses and may replace them with optimized download responses.

"""
import copy
import collections
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django_downloadview.response import DownloadResponse
from django_downloadview.utils import import_member


#: Sentinel value to detect whether configuration is to be loaded from Django
#: settings or not.
AUTO_CONFIGURE = object()


def is_download_response(response):
    """Return ``True`` if ``response`` is a download response.

    Current implementation returns True if ``response`` is an instance of
    :py:class:`django_downloadview.response.DownloadResponse`.

    """
    return isinstance(response, DownloadResponse)


class BaseDownloadMiddleware(object):
    """Base (abstract) Django middleware that handles download responses.

    Subclasses **must** implement :py:meth:`process_download_response` method.

    """
    def is_download_response(self, response):
        """Return True if ``response`` can be considered as a file download.

        By default, this method uses
        :py:func:`django_downloadview.middlewares.is_download_response`.
        Override this method if you want a different behaviour.

        """
        return is_download_response(response)

    def process_response(self, request, response):
        """Call `process_download_response()` if ``response`` is download."""
        if self.is_download_response(response):
            return self.process_download_response(request, response)
        return response

    def process_download_response(self, request, response):
        """Handle file download response."""
        raise NotImplementedError()


class RealDownloadMiddleware(BaseDownloadMiddleware):
    """Download middleware that cannot handle virtual files."""
    def is_download_response(self, response):
        """Return True for DownloadResponse, except for "virtual" files.

        This implementation cannot handle files that live in memory or which
        are to be dynamically iterated over. So, we capture only responses
        whose file attribute have either an URL or a file name.

        """
        if super(RealDownloadMiddleware, self).is_download_response(response):
            try:
                return response.file.url or response.file.name
            except AttributeError:
                return False
            else:
                return True
        return False


class DownloadDispatcherMiddleware(BaseDownloadMiddleware):
    "Download middleware that dispatches job to several middleware instances."
    def __init__(self, middlewares=AUTO_CONFIGURE):
        #: List of children middlewares.
        self.middlewares = middlewares
        if self.middlewares is AUTO_CONFIGURE:
            self.auto_configure_middlewares()

    def auto_configure_middlewares(self):
        """Populate :attr:`middlewares` from
        ``settings.DOWNLOADVIEW_MIDDLEWARES``."""
        for (key, import_string, kwargs) in getattr(settings,
                                                    'DOWNLOADVIEW_MIDDLEWARES',
                                                    []):
            factory = import_member(import_string)
            middleware = factory(**kwargs)
            self.middlewares.append((key, middleware))

    def process_download_response(self, request, response):
        """Dispatches job to children middlewares."""
        for (key, middleware) in self.middlewares:
            response = middleware.process_response(request, response)
        return response


class SmartDownloadMiddleware(BaseDownloadMiddleware):
    """Easy to configure download middleware."""
    def __init__(self,
                 backend_factory=AUTO_CONFIGURE,
                 backend_options=AUTO_CONFIGURE):
        """Constructor."""
        #: :class:`DownloadDispatcher` instance that can hold multiple
        #: backend instances.
        self.dispatcher = DownloadDispatcherMiddleware(middlewares=[])
        #: Callable (typically a class) to instanciate backend (typically a
        #: :class:`DownloadMiddleware` subclass).
        self.backend_factory = backend_factory
        if self.backend_factory is AUTO_CONFIGURE:
            self.auto_configure_backend_factory()
        #: List of positional or keyword arguments to instanciate backend
        #: instances.
        self.backend_options = backend_options
        if self.backend_options is AUTO_CONFIGURE:
            self.auto_configure_backend_options()

    def auto_configure_backend_factory(self):
        "Assign :attr:`backend_factory` from ``settings.DOWNLOADVIEW_BACKEND``"
        try:
            self.backend_factory = import_member(settings.DOWNLOADVIEW_BACKEND)
        except AttributeError:
            raise ImproperlyConfigured('SmartDownloadMiddleware requires '
                                       'settings.DOWNLOADVIEW_BACKEND')

    def auto_configure_backend_options(self):
        """Populate :attr:`dispatcher` using :attr:`factory` and
        ``settings.DOWNLOADVIEW_RULES``."""
        try:
            options_list = copy.deepcopy(settings.DOWNLOADVIEW_RULES)
        except AttributeError:
            raise ImproperlyConfigured('SmartDownloadMiddleware requires '
                                       'settings.DOWNLOADVIEW_RULES')
        for key, options in enumerate(options_list):
            args = []
            kwargs = {}
            if isinstance(options, collections.Mapping):  # Using kwargs.
                kwargs = options
            else:
                args = options
            if 'backend' in kwargs:  # Specific backend for this rule.
                factory = import_member(kwargs['backend'])
                del kwargs['backend']
            else:  # Fallback to global backend.
                factory = self.backend_factory
            middleware_instance = factory(*args, **kwargs)
            self.dispatcher.middlewares.append((key, middleware_instance))

    def process_download_response(self, request, response):
        """Use :attr:`dispatcher` to process download response."""
        return self.dispatcher.process_download_response(request, response)


class NoRedirectionMatch(Exception):
    """Response object does not match redirection rules."""


class ProxiedDownloadMiddleware(RealDownloadMiddleware):
    """Base class for middlewares that use optimizations of reverse proxies."""
    def __init__(self, source_dir=None, source_url=None, destination_url=None):
        """Constructor."""
        self.source_dir = source_dir
        self.source_url = source_url
        self.destination_url = destination_url

    def get_redirect_url(self, response):
        """Return redirect URL for file wrapped into response."""
        url = None
        file_url = ''
        if self.source_url:
            try:
                file_url = response.file.url
            except AttributeError:
                pass
            else:
                if file_url.startswith(self.source_url):
                    file_url = file_url[len(self.source_url):]
                    url = file_url
        file_name = ''
        if url is None and self.source_dir:
            try:
                file_name = response.file.name
            except AttributeError:
                pass
            else:
                if file_name.startswith(self.source_dir):
                    file_name = os.path.relpath(file_name, self.source_dir)
                    url = file_name.replace(os.path.sep, '/')
        if url is None:
            message = ("""Couldn't capture/convert file attributes into a """
                       """redirection. """
                       """``source_url`` is "%(source_url)s", """
                       """file's URL is "%(file_url)s". """
                       """``source_dir`` is "%(source_dir)s", """
                       """file's name is "%(file_name)s". """
                       % {'source_url': self.source_url,
                          'file_url': file_url,
                          'source_dir': self.source_dir,
                          'file_name': file_name})
            raise NoRedirectionMatch(message)
        return '/'.join((self.destination_url.rstrip('/'), url.lstrip('/')))
