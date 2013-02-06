# coding=utf8
"""Demo download views."""
from cStringIO import StringIO
from os.path import abspath, dirname, join

from django.core.files.storage import FileSystemStorage

from django_downloadview.files import VirtualFile
from django_downloadview.views import (ObjectDownloadView,
                                       PathDownloadView,
                                       StorageDownloadView,
                                       VirtualDownloadView)

from demoproject.download.models import Document


# Some initializations.

#: Directory containing code of :py:module:`demoproject.download.views`.
app_dir = dirname(abspath(__file__))

#: Directory containing files fixtures.
fixtures_dir = join(app_dir, 'fixtures')

#: Path to a text file that says 'Hello world!'.
hello_world_path = join(fixtures_dir, 'hello-world.txt')

#: Storage for fixtures.
fixtures_storage = FileSystemStorage(location=fixtures_dir)


# Here are the views.

#: Pre-configured download view for :py:class:`Document` model.
download_document = ObjectDownloadView.as_view(model=Document)


#: Pre-configured view using a storage.
download_fixture_from_storage = StorageDownloadView.as_view(
    storage=fixtures_storage)


#: Direct download of one file, based on an absolute path.
#:
#: You could use this example as a shortcut, inside other views.
download_hello_world = PathDownloadView.as_view(path=hello_world_path)


class CustomPathDownloadView(PathDownloadView):
    """Example of customized PathDownloadView."""
    def get_path(self):
        """Convert relative path (provided in URL) into absolute path.

        Notice that this particularly simple use case is covered by
        :py:class:`django_downloadview.views.StorageDownloadView`.

        .. warning::

           If you are doing such things, make the path secure! Prevent users
           to download files anywhere in the filesystem.

        """
        path = super(CustomPathDownloadView, self).get_path()
        return join(fixtures_dir, path)

#: Pre-configured :py:class:`CustomPathDownloadView`.
download_fixture_from_path = CustomPathDownloadView.as_view()


class StringIODownloadView(VirtualDownloadView):
    """Sample download view using StringIO object."""
    def get_file(self):
        """Return wrapper on StringIO object."""
        file_obj = StringIO(u"Hello world!\n")
        return VirtualFile(file_obj, name='hello-world.txt')

#: Pre-configured view that serves "Hello world!" via a StringIO.
download_generated_hello_world = StringIODownloadView.as_view()
