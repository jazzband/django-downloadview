# coding=utf-8
"""Views."""
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.http import HttpResponseNotModified
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.static import was_modified_since

import requests

from django_downloadview import files
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
        """Return a file wrapper instance."""
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

    def not_modified_response(self, *args, **kwargs):
        """Return :py:class:`django.http.HttpResponseNotModified` instance."""
        content_type = self.file_instance.content_type
        return HttpResponseNotModified(content_type=content_type)

    def download_response(self, *args, **kwargs):
        """Return :py:class:`DownloadResponse` instance."""
        response_kwargs = {'file_instance': self.file_instance,
                           'attachment': self.attachment,
                           'basename': self.get_basename()}
        response_kwargs.update(kwargs)
        response = self.response_class(**response_kwargs)
        return response

    def render_to_response(self, *args, **kwargs):
        """Return a download response.

        Respects the "HTTP_IF_MODIFIED_SINCE" header if any. In that case, uses
        :py:meth:`was_modified_since` and :py:meth:`not_modified_response`.

        Else, uses :py:meth:`download_response` to return a download response.

        """
        self.file_instance = self.get_file()
        # Respect the If-Modified-Since header.
        since = self.request.META.get('HTTP_IF_MODIFIED_SINCE', None)
        if since is not None:
            if not self.was_modified_since(self.file_instance, since):
                return self.not_modified_response(*args, **kwargs)
        # Return download response.
        return self.download_response(*args, **kwargs)


class BaseDownloadView(DownloadMixin, View):
    def get(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        return self.render_to_response()


class PathDownloadView(BaseDownloadView):
    """Serve a file using filename."""
    #: Server-side name (including path) of the file to serve.
    #:
    #: Filename is supposed to be an absolute filename of a file located on the
    #: local filesystem.
    path = None

    #: Name of the URL argument that contains path.
    path_url_kwarg = 'path'

    def get_path(self):
        """Return actual path of the file to serve.

        Default implementation simply returns view's :py:attr:`path`.

        Override this method if you want custom implementation.
        As an example, :py:attr:`path` could be relative and your custom
        :py:meth:`get_path` implementation makes it absolute.

        """
        return self.kwargs.get(self.path_url_kwarg, self.path)

    def get_file(self):
        """Use path to return wrapper around file to serve."""
        return File(open(self.get_path()))


class StorageDownloadView(PathDownloadView):
    """Serve a file using storage and filename."""
    #: Storage the file to serve belongs to.
    storage = DefaultStorage()

    #: Path to the file to serve relative to storage.
    path = None  # Override docstring.

    def get_path(self):
        """Return path of the file to serve, relative to storage.

        Default implementation simply returns view's :py:attr:`path`.

        Override this method if you want custom implementation.

        """
        return super(StorageDownloadView, self).get_path()

    def get_file(self):
        """Use path and storage to return wrapper around file to serve."""
        return files.StorageFile(self.storage, self.get_path())


class VirtualDownloadView(BaseDownloadView):
    """Serve not-on-disk or generated-on-the-fly file.

    Use this class to serve :py:class:`StringIO` files.

    Override the :py:meth:`get_file` method to customize file wrapper.

    """
    def get_file(self):
        """Return wrapper."""
        raise NotImplementedError()

    def was_modified_since(self, file_instance, since):
        """Delegate to file wrapper's was_modified_since, or return True.

        This is the implementation of an edge case: when files are generated
        on the fly, we cannot guess whether they have been modified or not.
        If the file wrapper implements ``was_modified_since()`` method, then we
        trust it. Otherwise it is safer to suppose that the file has been
        modified.

        This behaviour prevents file size to be computed on the Django side.
        Because computing file size means iterating over all the file contents,
        and we want to avoid that whenever possible. As an example, it could
        reduce all the benefits of working with dynamic file generators...
        which is a major feature of virtual files.

        """
        try:
            return file_instance.was_modified_since(since)
        except (AttributeError, NotImplementedError):
            return True


class HTTPDownloadView(BaseDownloadView):
    """Proxy files that live on remote servers."""
    #: URL to download (the one we are proxying).
    url = u''

    #: Additional keyword arguments for request handler.
    request_kwargs = {}

    def get_request_factory(self):
        """Return request factory to perform actual HTTP request."""
        return requests.get

    def get_request_kwargs(self):
        """Return keyword arguments for use with request factory."""
        return self.request_kwargs

    def get_url(self):
        """Return remote file URL (the one we are proxying)."""
        return self.url

    def get_file(self):
        """Return wrapper which has an ``url`` attribute."""
        return files.HTTPFile(request_factory=self.get_request_factory(),
                              name=self.get_basename(),
                              url=self.get_url(),
                              **self.get_request_kwargs())


class ObjectDownloadView(DownloadMixin, BaseDetailView):
    """Download view for models which contain a FileField.

    This class extends BaseDetailView, so you can use its arguments to target
    the instance to operate on: slug, slug_kwarg, model, queryset...
    See Django's DetailView reference for details.

    In addition to BaseDetailView arguments, you can set arguments related to
    the file to be downloaded.

    The main one is ``file_field``.

    The other arguments are provided for convenience, in case your model holds
    some (deserialized) metadata about the file, such as its basename, its
    modification time, its MIME type... These fields may be particularly handy
    if your file storage is not the local filesystem.

    """
    #: Name of the model's attribute which contains the file to be streamed.
    #: Typically the name of a FileField.
    file_field = 'file'

    #: Optional name of the model's attribute which contains the basename.
    basename_field = None

    #: Optional name of the model's attribute which contains the encoding.
    encoding_field = None

    #: Optional name of the model's attribute which contains the MIME type.
    mime_type_field = None

    #: Optional name of the model's attribute which contains the charset.
    charset_field = None

    #: Optional name of the model's attribute which contains the modification
    # time.
    modification_time_field = None

    #: Optional name of the model's attribute which contains the size.
    size_field = None

    def get_file(self):
        """Return FieldFile instance."""
        file_instance = getattr(self.object, self.file_field)
        for field in ('encoding', 'mime_type', 'charset', 'modification_time',
                      'size'):
            model_field = getattr(self, '%s_field' % field, False)
            if model_field:
                value = getattr(self.object, model_field)
                setattr(file_instance, field, value)
        return file_instance

    def get_basename(self):
        """Return client-side filename."""
        basename = super(ObjectDownloadView, self).get_basename()
        if basename is None:
            field = 'basename'
            model_field = getattr(self, '%s_field' % field, False)
            if model_field:
                basename = getattr(self.object, model_field)
        return basename
