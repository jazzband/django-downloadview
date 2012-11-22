"""Views."""
import mimetypes
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.http import Http404, HttpResponseNotModified
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.static import was_modified_since

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

    def get_file(self):
        """Return a django.core.files.File object, which is to be served."""
        raise NotImplementedError()

    def get_filename(self):
        """Return server-side absolute filename of the file to serve.

        "filename" is used server-side, whereas "basename" is the filename
        that the client receives for download (i.e. used client side).

        """
        file_obj = self.get_file()
        return file_obj.name

    def get_basename(self):
        """Return client-side filename, without path, of the file to be served.

        "basename" is the filename that the client receives for download,
        whereas "filename" is used server-side.

        The base implementation returns the basename of the server-side
        filename.

        You may override this method to change the behavior.

        """
        return os.path.basename(self.get_filename())

    def get_file_wrapper(self):
        """Return a wsgiref.util.FileWrapper instance for the file to serve."""
        try:
            return self.file_wrapper
        except AttributeError:
            self.file_wrapper = FileWrapper(self.get_file())
            return self.file_wrapper

    def get_mime_type(self):
        """Return mime-type of the file to serve."""
        try:
            return self.mime_type
        except AttributeError:
            basename = self.get_basename()
            self.mime_type, self.encoding = mimetypes.guess_type(basename)
            if not self.mime_type:
                self.mime_type = 'application/octet-stream'
            return self.mime_type

    def get_encoding(self):
        """Return encoding of the file to serve."""
        try:
            return self.encoding
        except AttributeError:
            filename = self.get_filename()
            self.mime_type, self.encoding = mimetypes.guess_type(filename)
            return self.encoding

    def get_charset(self):
        """Return the charset of the file to serve."""
        try:
            return self.charset
        except AttributeError:
            self.charset = settings.DEFAULT_CHARSET
        return self.charset

    def get_modification_time(self):
        """Return last modification time of the file to serve."""
        try:
            return self.modification_time
        except AttributeError:
            self.stat = os.stat(self.get_filename())
            self.modification_time = self.stat.st_mtime
            return self.modification_time

    def get_size(self):
        """Return the size (in bytes) of the file to serve."""
        try:
            return self.size
        except AttributeError:
            try:
                self.size = self.stat.st_size
            except AttributeError:
                self.size = os.path.getsize(self.get_filename())
            return self.size

    def render_to_response(self, **kwargs):
        """Returns a response with a file as attachment."""
        mime_type = self.get_mime_type()
        charset = self.get_charset()
        content_type = '%s; charset=%s' % (mime_type, charset)
        modification_time = self.get_modification_time()
        size = self.get_size()
        # Respect the If-Modified-Since header.
        if_modified_since = self.request.META.get('HTTP_IF_MODIFIED_SINCE',
                                                  None)
        if not was_modified_since(if_modified_since, modification_time, size):
            return HttpResponseNotModified(content_type=content_type)
        # Stream the file.
        filename = self.get_filename()
        basename = self.get_basename()
        encoding = self.get_encoding()
        wrapper = self.get_file_wrapper()
        response_kwargs = {'content': wrapper,
                           'content_type': content_type,
                           'content_length': size,
                           'filename': filename,
                           'basename': basename,
                           'content_encoding': encoding,
                           'expires': None}
        response_kwargs.update(kwargs)
        response = self.response_class(**response_kwargs)
        # Do not close the file as response class may need it open: the wrapper
        # is an iterator on the content of the file.
        # Garbage collector will close the file.
        return response


class DownloadView(DownloadMixin, View):
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
        try:
            return self._file
        except AttributeError:
            try:
                if self.storage:
                    self._file = self.storage.open(self.filename)
                else:
                    self._file = File(open(self.filename))
                return self._file
            except IOError:
                raise Http404()

    def get(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        return self.render_to_response()


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

    def get_object(self):
        """Return model instance, using cache or a get_queryset()."""
        try:
            return self._object
        except AttributeError:
            self._object = super(ObjectDownloadView, self).get_object()
        return self._object

    object = property(get_object)

    def get_fieldfile(self):
        """Return FieldFile instance (i.e. FileField attribute)."""
        try:
            return self.fieldfile
        except AttributeError:
            self.fieldfile = getattr(self.object, self.file_field)
            return self.fieldfile

    def get_file(self):
        """Return File instance."""
        return self.get_fieldfile().file

    def get_filename(self):
        """Return absolute filename."""
        file_obj = self.get_file()
        return file_obj.name

    def get_basename(self):
        """Return client-side filename."""
        if self.basename_field:
            return getattr(self.object, self.basename_field)
        else:
            return super(ObjectDownloadView, self).get_basename()

    def get_mime_type(self):
        """Return mime-type."""
        if self.mime_type_field:
            return getattr(self.object, self.mime_type_field)
        else:
            return super(ObjectDownloadView, self).get_mime_type()

    def get_charset(self):
        """Return charset of the file to serve."""
        if self.charset_field:
            return getattr(self.object, self.charset_field)
        else:
            return super(ObjectDownloadView, self).get_charset()

    def get_encoding(self):
        """Return encoding of the file to serve."""
        if self.encoding_field:
            return getattr(self.object, self.encoding_field)
        else:
            return super(ObjectDownloadView, self).get_encoding()

    def get_modification_time(self):
        """Return last modification time of the file to serve."""
        if self.modification_time_field:
            return getattr(self.object, self.modification_time_field)
        else:
            return super(ObjectDownloadView, self).get_modification_time()

    def get_size(self):
        """Return size of the file to serve."""
        if self.size_field:
            return getattr(self.object, self.size_field)
        else:
            return self.get_fieldfile().size

    def get(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        return self.render_to_response()
