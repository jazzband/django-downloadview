# -*- coding: utf-8 -*-
"""Base material for download views: :class:`DownloadMixin` and
:class:`BaseDownloadView`"""
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
    attachment = True

    #: Client-side filename, if only file is returned as attachment.
    basename = None

    def get_file(self):
        """Return a file wrapper instance.

        Raises :class:`~django_downloadview.exceptions.FileNotFound` if file
        does not exist.

        """
        raise NotImplementedError()

    def get_basename(self):
        return self.basename

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
                modification_time = file_instance.modified_time
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
