# -*- coding: utf-8 -*-
""":class:`PathDownloadView`."""
import os

from django.core.files import File

from django_downloadview.exceptions import FileNotFound
from django_downloadview.views.base import BaseDownloadView


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
        filename = self.get_path()
        if not os.path.isfile(filename):
            raise FileNotFound('File "{0}" does not exists'.format(filename))
        return File(open(filename, 'rb'))
