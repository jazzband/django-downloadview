"""File wrappers for use as exchange data between views and responses."""
from django.core.files import File


class StorageFile(File):
    """A file in a Django storage.

    This class looks like :py:class:`django.db.models.fields.files.FieldFile`,
    but unrelated to model instance.

    """
    def __init__(self, storage, name, file=None):
        """Constructor.

        storage:
          Some :py:class:`django.core.files.storage.Storage` instance.

        name:
          File identifier in storage, usually a filename as a string.

        """
        self.storage = storage
        self.name = name
        self.file = file

    def _get_file(self):
        """Getter for :py:attr:``file`` property."""
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    def _set_file(self, file):
        """Setter for :py:attr:``file`` property."""
        self._file = file

    def _del_file(self):
        """Deleter for :py:attr:``file`` property."""
        del self._file

    #: Required by django.core.files.utils.FileProxy.
    file = property(_get_file, _set_file, _del_file)

    def open(self, mode='rb'):
        """Retrieves the specified file from storage and return open() result.

        Proxy to self.storage.open(self.name, mode).

        """
        return self.storage.open(self.name, mode)

    def save(self, content):
        """Saves new content to the file.

        Proxy to self.storage.save(self.name).

        The content should be a proper File object, ready to be read from the
        beginning.

        """
        return self.storage.save(self.name, content)

    @property
    def path(self):
        """Return a local filesystem path which is suitable for open().

        Proxy to self.storage.path(self.name).

        May raise NotImplementedError if storage doesn't support file access
        with Python's built-in open() function

        """
        return self.storage.path(self.name)

    def delete(self):
        """Delete the specified file from the storage system.

        Proxy to self.storage.delete(self.name).

        """
        return self.storage.delete(self.name)

    def exists(self):
        """Return True if file already exists in the storage system.

        If False, then the name is available for a new file.

        """
        return self.storage.exists(self.name)

    @property
    def size(self):
        """Return the total size, in bytes, of the file.

        Proxy to self.storage.size(self.name).

        """
        return self.storage.size(self.name)

    @property
    def url(self):
        """Return an absolute URL where the file's contents can be accessed.

        Proxy to self.storage.url(self.name).

        """
        return self.storage.url(self.name)

    @property
    def accessed_time(self):
        """Return the last accessed time (as datetime object) of the file.

        Proxy to self.storage.accessed_time(self.name).

        """
        return self.storage.accessed(self.name)

    @property
    def created_time(self):
        """Return the creation time (as datetime object) of the file.

        Proxy to self.storage.created_time(self.name).

        """
        return self.storage.created_time(self.name)

    @property
    def modified_time(self):
        """Return the last modification time (as datetime object) of the file.

        Proxy to self.storage.modified_time(self.name).

        """
        return self.storage.modified_time(self.name)
