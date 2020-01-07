from django.core.files.storage import FileSystemStorage

from django_downloadview import StorageDownloadView

storage = FileSystemStorage()


#: Serve file using ``path`` argument.
static_path = StorageDownloadView.as_view(storage=storage)


class DynamicStorageDownloadView(StorageDownloadView):
    """Serve file of storage by path.upper()."""

    def get_path(self):
        """Return uppercase path."""
        return super(DynamicStorageDownloadView, self).get_path().upper()


dynamic_path = DynamicStorageDownloadView.as_view(storage=storage)
