"""HttpResponse subclasses."""
import os
import mimetypes

from django.conf import settings
from django.http import HttpResponse


class DownloadResponse(HttpResponse):
    """File download response.

    ``content`` attribute is supposed to be a file object wrapper, which makes
    this response "lazy".

    """
    def __init__(self, file_instance, attachment=True, basename=None,
                 status=200, content_type=None, size=None):
        """Constructor.

        It differs a bit from HttpResponse constructor.

        file_instance:
          A file wrapper object. Could be a FieldFile.

        attachement:
          Boolean, whether to return the file as attachment or not. Affects
          "Content-Disposition" header.
          Defaults to ``True``.

        basename:
          Unicode. Only used if ``attachment`` is ``True``. Client-side name
          of the file to stream. Affects "Content-Disposition" header.
          Defaults to basename(``file_instance.name``).

        status:
          HTTP status code.
          Defaults to 200.

        content_type:
          Value for "Content-Type" header.
          If ``None``, then mime-type and encoding will be populated by the
          response (default implementation uses mimetypes, based on file name).
          Defaults is ``None``.

        size:
          Size of the file response

        """
        self.file = file_instance
        super(DownloadResponse, self).__init__(content=self.file,
                                               status=status,
                                               content_type=content_type)
        self.basename = basename
        self.attachment = attachment
        self.content_type = content_type
        self.size = size
        if not content_type:
            del self['Content-Type']  # Will be set later.
        # Apply default headers.
        for header, value in self.default_headers.items():
            if not header in self:
                self[header] = value  # Does self support setdefault?

    @property
    def default_headers(self):
        """Return dictionary of automatically-computed headers.

        Uses an internal ``_default_headers`` cache.
        Default values are computed if only cache hasn't been set.

        """
        try:
            return self._default_headers
        except AttributeError:
            headers = {}
            headers['Content-Type'] = self.get_content_type()
            headers['Content-Length'] = self.get_size()
            if self.attachment:
                headers['Content-Disposition'] = 'attachment; filename=%s' \
                                                 % self.get_basename()
            self._default_headers = headers
            return self._default_headers

    def items(self):
        """Return iterable of (header, value).

        This method is called by http handlers just before WSGI's
        start_response() is called... but it is not called by
        django.test.ClientHandler! :'(

        """
        return super(DownloadResponse, self).items()

    def get_basename(self):
        """Return basename."""
        if self.attachment and self.basename:
            return self.basename
        else:
            return os.path.basename(self.file.name)

    def get_content_type(self):
        """Return a suitable "Content-Type" header for ``self.file``."""
        if not self.content_type:
            try:
                return self.file.content_type
            except AttributeError:
                content_type_template = '%(mime_type)s; charset=%(charset)s'
                return content_type_template % {
                    'mime_type': self.get_mime_type(),
                    'charset': self.get_charset()}
        return self.content_type

    def get_mime_type(self):
        """Return mime-type of the file."""
        default_mime_type = 'application/octet-stream'
        basename = self.get_basename()
        mime_type, encoding = mimetypes.guess_type(basename)
        return mime_type or default_mime_type

    def get_encoding(self):
        """Return encoding of the file to serve."""
        basename = self.get_basename()
        mime_type, encoding = mimetypes.guess_type(basename)
        return encoding

    def get_charset(self):
        """Return the charset of the file to serve."""
        return settings.DEFAULT_CHARSET

    def get_size(self):
        """Return the size of the file to serve."""
        if not self.size:
            self.size = self.file.size
        return self.size


def is_download_response(response):
    """Return ``True`` if ``response`` is a download response.

    Current implementation returns True if ``response`` is an instance of
    :py:class:`django_downloadview.response.DownloadResponse`.

    """
    return isinstance(response, DownloadResponse)
