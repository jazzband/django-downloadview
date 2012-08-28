import mimetypes
import os
import shutil
from wsgiref.util import FileWrapper

from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.static import was_modified_since


class DownloadMixin(object):
    response_class = HttpResponse

    def get_file(self):
        """Return a django.core.files.File object, which is to be served."""
        raise NotImplementedError()

    def get_filename(self):
        """Return absolute filename."""
        file_obj = self.get_file()
        return file_obj.name

    def get_file_wrapper(self):
        """Return a wsgiref.util.FileWrapper instance for the file to serve."""
        try:
            return self.file_wrapper
        except AttributeError:
            self.file_wrapper = FileWrapper(self.get_file())
            return self.file_wrapper

    def get_mime_type(self):
        """Return mime-type."""
        try:
            return self.mime_type
        except AttributeError:
            filename = self.get_filename()
            self.mime_type, self.encoding = mimetypes.guess_type(filename)
            if not self.mime_type:
                self.mime_type = 'application/octet-stream'
            return self.mime_type

    def get_encoding(self):
        """Return encoding of self.file."""
        try:
            return self.encoding
        except AttributeError:
            filename = self.get_filename()
            self.mime_type, self.encoding = mimetypes.guess_type(filename)
            return self.encoding

    def get_modification_time(self):
        """Return last modification time of self.file."""
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

    def render_to_response(self, **response_kwargs):
        """Returns a response with a file as attachment."""
        mime_type = self.get_mime_type()
        modification_time = self.get_modification_time()
        size = self.get_size()
        # Respect the If-Modified-Since header.
        if_modified_since = self.request.META.get('HTTP_IF_MODIFIED_SINCE', None)
        if not was_modified_since(if_modified_since, modification_time, size):
            return HttpResponseNotModified(mimetype=mime_type)
        # Stream the file.
        filename = self.get_filename()
        basename = os.path.basename(filename)
        encoding = self.get_encoding()
        wrapper = self.get_file_wrapper()
        response = self.response_class(wrapper, content_type=mime_type,
                                       mimetype=mime_type)
        response['Content-Length'] = size
        # Do not call fsock.close() as HttpResponse needs it open.
        # Garbage collector will close it.
        response['Content-Disposition'] = 'attachment; filename=%s' % basename
        return response


class DownloadView(DownloadMixin, View):
    filename = None
    storage = DefaultStorage()

    def get_file(self):
        """Return a file object for the file to serve."""
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
                raise Http404

    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class ObjectDownloadView(DownloadMixin, BaseDetailView):
    file_field = 'file'

    def get_fieldfile(self):
        self.object = self.get_object()
        try:
            return self.fieldfile
        except AttributeError:
            self.fieldfile = getattr(self.object, self.file_field)
            return self.fieldfile

    def get_file(self):
        return self.get_fieldfile().file

    def get_size(self):
        return self.get_fieldfile().size

    def get(self, request, *args, **kwargs):
        return self.render_to_response()
