from os.path import abspath, basename
import shutil

from django.core.files import File
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView


class DownloadMixin(object):
    file = None
    response_class = HttpResponse

    def get_mime_type(self):
        """Return mime-type of self.file."""
        return 'application/octet-stream'

    def render_to_response(self, **response_kwargs):
        """Returns a response with a file as attachment."""
        mime_type = self.get_mime_type()
        if isinstance(self.file, File):
            absolute_filename = self.file.name
        else:
            absolute_filename = abspath(self.file)
        filename = basename(absolute_filename)
        response = self.response_class(mimetype=mime_type)
        # Open file as read binary.
        with open(absolute_filename, 'rb') as f:
            shutil.copyfileobj(f, response)
        # Do not call fsock.close() as  HttpResponse needs it open
        # Garbage collector will close it
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


class DownloadView(DownloadMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class ObjectDownloadView(DownloadMixin, BaseDetailView):
    file_field = 'file'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.file = getattr(self.object, self.file_field)
        return self.render_to_response()
