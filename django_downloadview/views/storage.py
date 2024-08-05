"""Stream files from storage."""

from django.core.files.storage import DefaultStorage

from django_downloadview.files import StorageFile
from django_downloadview.views.path import PathDownloadView


class StorageDownloadView(PathDownloadView):
    """Serve a file using storage and filename."""

    #: Storage the file to serve belongs to.
    storage = DefaultStorage()

    #: Path to the file to serve relative to storage.
    path = None  # Override docstring.

    def get_file(self):
        """Return :class:`~django_downloadview.files.StorageFile` instance."""
        return StorageFile(self.storage, self.get_path())
