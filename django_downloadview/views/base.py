# -*- coding: utf-8 -*-
"""Base material for download views: :class:`DownloadMixin` and
:class:`BaseDownloadView`"""
import calendar

from django.http import HttpResponseNotModified, Http404
from django.views.generic.base import View
from django.views.static import was_modified_since

from django_downloadview import exceptions
from django_downloadview.response import DownloadResponse


class DownloadMixin(object):
    """Placeholders and base implementation to create file download views.

    .. note::

       This class does not inherit from
       :py:class:`django.views.generic.base.View`.

    The :py:meth:`get_file` method is a placeholder subclasses must implement.
    Base implementation raises ``NotImplementedError``.

    Other methods provide a base implementation that use the file wrapper
    returned by :py:meth:`get_file`.

    """
    #: Response class, to be used in :py:meth:`render_to_response`.
    response_class = DownloadResponse

    #: Whether to return the response as attachment or not.
    #:
    #: When ``True`` (the default), the view returns file "as attachment",
    #: which usually triggers a "Save the file as ..." prompt.
    #:
    #: When ``False``, the view returns file "inline", as if it was an element
    #: of the current page.
    #:
    #: .. note::
    #:
    #:    The actual behaviour client-side depends on the browser and its
    #:    configuration.
    #:
    #: In fact, affects the "Content-Disposition" header via :attr:`response's
    #: attachment attribute
    #: <django_downloadview.response.DownloadResponse.attachment>`.
    attachment = True

    #: Client-side filename, if only file is returned as attachment.
    basename = None

    #: File's mime type.
    #: If ``None`` (the default), then the file's mime type will be guessed via
    #: :mod:`mimetypes`.
    mimetype = None

    #: File's encoding.
    #: If ``None`` (the default), then the file's encoding will be guessed via
    #: :mod:`mimetypes`.
    encoding = None

    def get_file(self):
        """Return a file wrapper instance.

        Raises :class:`~django_downloadview.exceptions.FileNotFound` if file
        does not exist.

        """
        raise NotImplementedError()

    def get_basename(self):
        """Return :attr:`basename`.

        Override this method if you need more dynamic basename.

        """
        return self.basename

    def get_mimetype(self):
        """Return :attr:`mimetype`.

        Override this method if you need more dynamic mime type.

        """
        return self.mimetype

    def get_encoding(self):
        """Return :attr:`encoding`.

        Override this method if you need more dynamic encoding.

        """
        return self.encoding

    def was_modified_since(self, file_instance, since):
        """Return True if ``file_instance`` was modified after ``since``.

        Uses file wrapper's ``was_modified_since`` if available, with value of
        ``since`` as positional argument.

        Else, fallbacks to default implementation, which uses
        :py:func:`django.views.static.was_modified_since`.

        Django's ``was_modified_since`` function needs a datetime and a size.
        It is passed ``modified_time`` and ``size`` attributes from file
        wrapper. If file wrapper does not support these attributes
        (``AttributeError`` or ``NotImplementedError`` is raised), then
        the file is considered as modified and ``True`` is returned.

        """
        try:
            return file_instance.was_modified_since(since)
        except (AttributeError, NotImplementedError):
            try:
                modification_time = calendar.timegm(
                    file_instance.modified_time.utctimetuple())
                size = file_instance.size
            except (AttributeError, NotImplementedError):
                return True
            else:
                return was_modified_since(since, modification_time, size)

    def not_modified_response(self, *response_args, **response_kwargs):
        """Return :class:`django.http.HttpResponseNotModified` instance."""
        return HttpResponseNotModified(*response_args, **response_kwargs)

    def download_response(self, *response_args, **response_kwargs):
        """Return :class:`~django_downloadview.response.DownloadResponse`."""
        response_kwargs.setdefault('file_instance', self.file_instance)
        response_kwargs.setdefault('attachment', self.attachment)
        response_kwargs.setdefault('basename', self.get_basename())
        response_kwargs.setdefault('file_mimetype', self.get_mimetype())
        response_kwargs.setdefault('file_encoding', self.get_encoding())
        response = self.response_class(*response_args, **response_kwargs)
        return response

    def file_not_found_response(self):
        """Raise Http404."""
        raise Http404()

    def render_to_response(self, *response_args, **response_kwargs):
        """Return "download" response (if everything is ok).

        Return :meth:`file_not_found_response` if file does not exist.

        Respects the "HTTP_IF_MODIFIED_SINCE" header if any. In that case, uses
        :py:meth:`was_modified_since` and :py:meth:`not_modified_response`.

        Else, uses :py:meth:`download_response` to return a download response.

        """
        try:
            self.file_instance = self.get_file()
        except exceptions.FileNotFound:
            return self.file_not_found_response()
        # Respect the If-Modified-Since header.
        since = self.request.META.get('HTTP_IF_MODIFIED_SINCE', None)
        if since is not None:
            if not self.was_modified_since(self.file_instance, since):
                return self.not_modified_response(**response_kwargs)
        # Return download response.
        return self.download_response(*response_args, **response_kwargs)


class BaseDownloadView(DownloadMixin, View):
    """A base :class:`DownloadMixin` that implements :meth:`get`."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        return self.render_to_response()
