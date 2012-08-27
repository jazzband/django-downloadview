from os.path import abspath, basename
import shutil

from django.http import HttpResponse
from django.views.generic.base import View


class DownloadMixin(object):
    file = None
    response_class = HttpResponse

    def get_mime_type(self, file):
        """Return mime-type of file."""
        return 'application/octet-stream'

    def render_to_response(self, file, **response_kwargs):
        """Returns a response with a file as attachment."""
        mime_type = self.get_mime_type(file)
        absolute_filename = abspath(file)
        filename = basename(file)
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
        return self.render_to_response(self.file)
