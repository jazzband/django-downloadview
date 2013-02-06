# coding=utf8
"""Demo download views."""
from os.path import abspath, dirname, join

from django_downloadview.views import ObjectDownloadView, PathDownloadView

from demoproject.download.models import Document


# Some initializations.

app_dir = dirname(abspath(__file__))
"""Directory containing code of :py:module:`demoproject.download.views`."""

fixtures_dir = join(app_dir, 'fixtures')
"""Directory containing files fixtures."""

hello_world_path = join(fixtures_dir, 'hello-world.txt')
"""Path to a text file that says 'Hello world!'."""


# Here are the views.

download_hello_world = PathDownloadView.as_view(path=hello_world_path)
"""Direct download of one file, based on an absolute path.

You could use this example as a shortcut, inside other views.

"""


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

download_fixture_from_path = CustomPathDownloadView.as_view()
"""Pre-configured :py:class:`CustomPathDownloadView`."""


download_document = ObjectDownloadView.as_view(model=Document)
"""Pre-configured download view for :py:class:`Document` model."""
