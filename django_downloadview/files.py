# -*- coding: utf-8 -*-
"""File wrappers for use as exchange data between views and responses."""
from __future__ import absolute_import
from io import BytesIO
from six.moves.urllib.parse import urlparse

from django.core.files.base import File
from django.utils.encoding import force_bytes

import requests

from django_downloadview.io import BytesIteratorIO


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


class VirtualFile(File):
    """Wrapper for files that live in memory."""
    def __init__(self, file=None, name=u'', url='', size=None):
        """Constructor.

        file:
          File object. Typically an io.StringIO.

        name:
          File basename.

        url:
          File URL.

        """
        super(VirtualFile, self).__init__(file, name)
        self.url = url
        if size is not None:
            self._size = size

    def _get_size(self):
        try:
            return self._size
        except AttributeError:
            try:
                self._size = self.file.size
            except AttributeError:
                self._size = len(self.file.getvalue())
        return self._size

    def _set_size(self, value):
        return super(VirtualFile, self)._set_size(value)

    size = property(_get_size, _set_size)

    def __iter__(self):
        """Same as ``File.__iter__()`` but using ``force_bytes()``.

        See https://code.djangoproject.com/ticket/21321

        """
        # Iterate over this file-like object by newlines
        buffer_ = None
        for chunk in self.chunks():
            chunk_buffer = BytesIO(force_bytes(chunk))

            for line in chunk_buffer:
                if buffer_:
                    line = buffer_ + line
                    buffer_ = None

                # If this is the end of a line, yield
                # otherwise, wait for the next round
                if line[-1] in ('\n', '\r'):
                    yield line
                else:
                    buffer_ = line

        if buffer_ is not None:
            yield buffer_


class HTTPFile(File):
    """Wrapper for files that live on remote HTTP servers.

    Acts as a proxy.

    Uses https://pypi.python.org/pypi/requests.

    Always sets "stream=True" in requests kwargs.

    """
    def __init__(self, request_factory=requests.get, url='', name=u'',
                 **kwargs):
        self.request_factory = request_factory
        self.url = url
        if name is None:
            parts = urlparse(url)
            if parts.path:  # Name from path.
                self.name = parts.path.strip('/').rsplit('/', 1)[-1]
            else:  # Name from domain.
                self.name = parts.netloc
        else:
            self.name = name
        kwargs['stream'] = True
        self.request_kwargs = kwargs

    @property
    def request(self):
        try:
            return self._request
        except AttributeError:
            self._request = self.request_factory(self.url,
                                                 **self.request_kwargs)
            return self._request

    @property
    def file(self):
        try:
            return self._file
        except AttributeError:
            content = self.request.iter_content(decode_unicode=False)
            self._file = BytesIteratorIO(content)
            return self._file

    @property
    def size(self):
        """Return the total size, in bytes, of the file.

        Reads response's "content-length" header.

        """
        return self.request.headers['Content-Length']

    @property
    def content_type(self):
        """Return content type of the file (from original response)."""
        return self.request.headers['Content-Type']
