"""HttpResponse subclasses."""
from django.http import HttpResponse


class DownloadResponse(HttpResponse):
    """File download response."""
    def __init__(self, content, content_type, content_length, basename,
                 status=200, content_encoding=None, expires=None,
                 filename=None):
        """Constructor.

        It differs a bit from HttpResponse constructor.

        Required arguments:

        * ``content`` is supposed to be an iterable that can read the file.
          Consider :py:class:`wsgiref.util.FileWrapper`` as a good candidate.

        * ``content_type`` contains mime-type and charset of the file.
          It is used as "Content-Type" header.

        * ``content_length`` is the size, in bytes, of the file.
          It is used as "Content-Length" header.

        * ``basename`` is the client-side name of the file ("save as" name).
          It is used in "Content-Disposition" header.

        Optional arguments:

        * ``status`` is HTTP status code.

        * ``content_encoding`` is used for "Content-Encoding" header.

        * ``expires`` is a datetime.
          It is used to set the "Expires" header.

        * ``filename`` is the server-side name of the file.
          It may be used by decorators or middlewares to delegate the actual
          streaming to a more efficient server (i.e. Nginx, Lighttpd...).

        """
        super(DownloadResponse, self).__init__(content=content, status=status,
                                               content_type=content_type)
        self.filename = filename
        self.basename = basename
        self['Content-Length'] = content_length
        if content_encoding:
            self['Content-Encoding'] = content_encoding
        self.expires = expires
        if expires:
            self['Expires'] = expires
        self['Content-Disposition'] = 'attachment; filename=%s' % basename
