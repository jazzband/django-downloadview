# -*- coding: utf-8 -*-
""":py:class:`django.http.HttpResponse` subclasses."""
import os
import mimetypes
import re
import unicodedata
import six
from six.moves import urllib

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.encoding import force_str


def encode_basename_ascii(value):
    u"""Return US-ASCII encoded ``value`` for Content-Disposition header.

    >>> print(encode_basename_ascii(u'éà'))
    ea

    Spaces are converted to underscores.

    >>> print(encode_basename_ascii(' '))
    _

    Of course, ASCII values are not modified.

    >>> print(encode_basename_ascii('ea'))
    ea
    >>> print(encode_basename_ascii(b'ea'))
    ea

    """
    if isinstance(value, six.binary_type):
        value = value.decode('utf-8')
    ascii_basename = six.text_type(value)
    ascii_basename = unicodedata.normalize('NFKD', ascii_basename)
    ascii_basename = ascii_basename.encode('ascii', 'ignore')
    ascii_basename = ascii_basename.decode('ascii')
    ascii_basename = re.sub(r'[\s]', '_', ascii_basename)
    return ascii_basename


def encode_basename_utf8(value):
    u"""Return UTF-8 encoded ``value`` for use in Content-Disposition header.

    >>> print(encode_basename_utf8(u' .txt'))
    %20.txt

    >>> print(encode_basename_utf8(u'éà'))
    %C3%A9%C3%A0

    """
    return urllib.parse.quote(force_str(value))


def content_disposition(filename):
    u"""Return value of ``Content-Disposition`` header with 'attachment'.

    >>> print(content_disposition('demo.txt'))
    attachment; filename="demo.txt"

    If filename is empty, only "attachment" is returned.

    >>> print(content_disposition(''))
    attachment

    If filename contains non US-ASCII characters, the returned value contains
    UTF-8 encoded filename and US-ASCII fallback.

    >>> print(content_disposition(u'é.txt'))
    attachment; filename="e.txt"; filename*=UTF-8''%C3%A9.txt

    """
    if not filename:
        return 'attachment'
    ascii_filename = encode_basename_ascii(filename)
    utf8_filename = encode_basename_utf8(filename)
    if ascii_filename == utf8_filename:  # ASCII only.
        return "attachment; filename=\"{ascii}\"".format(ascii=ascii_filename)
    else:
        return "attachment; filename=\"{ascii}\"; filename*=UTF-8''{utf8}" \
               .format(ascii=ascii_filename,
                       utf8=utf8_filename)


class DownloadResponse(StreamingHttpResponse):
    """File download response (Django serves file, client downloads it).

    This is a specialization of :class:`django.http.StreamingHttpResponse`
    where :attr:`~django.http.StreamingHttpResponse.streaming_content` is a
    file wrapper.

    Constructor differs a bit from :class:`~django.http.response.HttpResponse`.

    Here are some highlights to understand internal mechanisms and motivations:

    * Let's start by quoting :pep:`3333` (WSGI specification):

          For large files, or for specialized uses of HTTP streaming,
          applications will usually return an iterator (often a
          generator-iterator) that produces the output in a block-by-block
          fashion.

    * Django WSGI handler (application implementation) returns response object
      (see :mod:`django.core.handlers.wsgi`).

    * :class:`django.http.HttpResponse` and subclasses are iterators.

    * In :class:`~django.http.StreamingHttpResponse`, the
      :meth:`~container.__iter__` implementation proxies to
      :attr:`~django.http.StreamingHttpResponse.streaming_content`.

    * In :class:`DownloadResponse` and subclasses, :attr:`streaming_content`
      is a :doc:`file wrapper </files>`. File wrapper is itself an iterator
      over actual file content, and it also encapsulates access to file
      attributes (size, name, ...).

    """
    def __init__(self, file_instance, attachment=True, basename=None,
                 status=200, content_type=None, file_mimetype=None,
                 file_encoding=None):
        """Constructor.

        :param content_type: Value for ``Content-Type`` header.
                             If ``None``, then mime-type and encoding will be
                             populated by the response (default implementation
                             uses :mod:`mimetypes`, based on file name).

        """
        #: A :doc:`file wrapper instance </files>`, such as
        #: :class:`~django.core.files.base.File`.
        self.file = file_instance
        super(DownloadResponse, self).__init__(streaming_content=self.file,
                                               status=status,
                                               content_type=content_type)

        #: Client-side name of the file to stream.
        #: Only used if ``attachment`` is ``True``.
        #: Affects ``Content-Disposition`` header.
        self.basename = basename

        #: Whether to return the file as attachment or not.
        #: Affects ``Content-Disposition`` header.
        self.attachment = attachment
        if not content_type:
            del self['Content-Type']  # Will be set later.

        #: Value for file's mimetype.
        #: If ``None`` (the default), then the file's mimetype will be guessed
        #: via Python's :mod:`mimetypes`. See :meth:`get_mime_type`.
        self.file_mimetype = file_mimetype

        #: Value for file's encoding. If ``None`` (the default), then the
        #: file's encoding will be guessed via Python's :mod:`mimetypes`. See
        #: :meth:`get_encoding`.
        self.file_encoding = file_encoding

        # Apply default headers.
        for header, value in self.default_headers.items():
            if header not in self:
                self[header] = value  # Does self support setdefault?

    @property
    def default_headers(self):
        """Return dictionary of automatically-computed headers.

        Uses an internal ``_default_headers`` cache.
        Default values are computed if only cache hasn't been set.

        ``Content-Disposition`` header is encoded according to `RFC 5987
        <http://tools.ietf.org/html/rfc5987>`_. See also
        http://stackoverflow.com/questions/93551/.

        """
        try:
            return self._default_headers
        except AttributeError:
            headers = {}
            headers['Content-Type'] = self.get_content_type()
            try:
                headers['Content-Length'] = self.file.size
            except (AttributeError, NotImplementedError):
                pass  # Generated files.
            if self.attachment:
                basename = self.get_basename()
                headers['Content-Disposition'] = content_disposition(basename)
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
        if self.basename:
            return self.basename
        else:
            return os.path.basename(self.file.name)

    def get_content_type(self):
        """Return a suitable "Content-Type" header for ``self.file``."""
        try:
            return self.file.content_type
        except AttributeError:
            content_type_template = '{mime_type}; charset={charset}'
            return content_type_template.format(mime_type=self.get_mime_type(),
                                                charset=self.get_charset())

    def get_mime_type(self):
        """Return mime-type of the file."""
        if self.file_mimetype is not None:
            return self.file_mimetype
        default_mime_type = 'application/octet-stream'
        basename = self.get_basename()
        mime_type, encoding = mimetypes.guess_type(basename)
        return mime_type or default_mime_type

    def get_encoding(self):
        """Return encoding of the file to serve."""
        if self.file_encoding is not None:
            return self.file_encoding
        basename = self.get_basename()
        mime_type, encoding = mimetypes.guess_type(basename)
        return encoding

    def get_charset(self):
        """Return the charset of the file to serve."""
        return settings.DEFAULT_CHARSET


class ProxiedDownloadResponse(HttpResponse):
    """Base class for internal redirect download responses.

    This base class makes it possible to identify several types of specific
    responses such as
    :py:class:`~django_downloadview.nginx.response.XAccelRedirectResponse`.

    """
