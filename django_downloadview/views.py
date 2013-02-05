"""Views."""
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.http import HttpResponseNotModified
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.static import was_modified_since

from django_downloadview.files import StorageFile
from django_downloadview.response import DownloadResponse


class DownloadMixin(object):
    """Placeholders and base implementation to create file download views.

    The get_file() method is a placeholder, which raises NotImplementedError
    in base implementation.

    The other methods provide an implementation that use the file object
    returned by get_file(), supposing the file is hosted on the local
    filesystem.

    You may override one or several methods to adapt the implementation to your
    use case.

    """
    #: Response class to be used in render_to_response().
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

    def get_size(self):
        return self.get_file().size

    def get_modification_time(self):
        return self.get_file().modified_time

    def get_content_type(self):
        return self.get_file().content_type

    def render_to_response(self, *args, **kwargs):
        """Returns a response with a file as attachment."""
        # Respect the If-Modified-Since header.
        file_instance = self.get_file()
        if_modified_since = self.request.META.get('HTTP_IF_MODIFIED_SINCE',
                                                  None)
        if if_modified_since is not None:
            modification_time = self.get_modification_time()
            size = self.get_size()
            if not was_modified_since(if_modified_since, modification_time,
                                      size):
                content_type = self.get_content_type()
                return HttpResponseNotModified(content_type=content_type)
        # Return download response.
        response_kwargs = {'file_instance': file_instance,
                           'attachment': self.attachment,
                           'basename': self.get_basename(),
                           'size': self.get_size(),
                           'content_type': self.get_content_type()}
        response_kwargs.update(kwargs)
        response = self.response_class(**response_kwargs)
        return response


class BaseDownloadView(DownloadMixin, View):
    def get(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        return self.render_to_response()


class StorageDownloadView():
    """Download a file from storage and filename."""
    storage = DefaultStorage()
    path = None


class SimpleDownloadView():
    """Download a file from filename."""
    path = None


class VirtualDownloadView():
    file_obj = None


class DownloadView(BaseDownloadView):
    """Download a file from storage and filename."""
    #: Server-side name (including path) of the file to serve.
    #:
    #: If ``storage`` is not None, then the filename will be passed to the
    #: storage, else filename is supposed to be an absolute filename of a file
    #: located on the local filesystem.
    filename = None

    #: Storage to use to fetch the file.
    #:
    #: Defaults to Django's DefaultStorage(), which itself defaults to a
    #: FileSystemStorage relative to settings.MEDIA_ROOT.
    #:
    #: The ``storage`` can be set to None, but you should use one. As an
    #: example, storage classes may encapsulate some security checks
    #: (FileSystemStorage actually refuses to serve files outside its root
    #: location).
    storage = DefaultStorage()

    def get_file(self):
        """Use filename and storage to return file object to serve."""
        if self.storage:
            return StorageFile(self.storage, self.filename)
        else:
            return File(open(self.filename))


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
