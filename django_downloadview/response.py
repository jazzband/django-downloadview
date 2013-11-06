# -*- coding: utf-8 -*-
""":py:class:`django.http.HttpResponse` subclasses."""
import os
import mimetypes

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse


class DownloadResponse(StreamingHttpResponse):
    """File download response (Django serves file, client downloads it).

    This is a specialization of :class:`django.http.StreamingHttpResponse`
    where :attr:`~django.http.StreamingHttpResponse.streaming_content` is a
    file wrapper.

    Constructor differs a bit from :class:`~django.http.response.HttpResponse`:

    ``file_instance``
        A :doc:`file wrapper instance </files>`, such as
        :class:`~django.core.files.base.File`.

    ``attachement``
        Boolean. Whether to return the file as attachment or not.
        Affects ``Content-Disposition`` header.

    ``basename``
        Unicode. Client-side name of the file to stream.
        Only used if ``attachment`` is ``True``.
        Affects ``Content-Disposition`` header.

    ``status``
        HTTP status code.

    ``content_type``
        Value for ``Content-Type`` header.
        If ``None``, then mime-type and encoding will be populated by the
        response (default implementation uses mimetypes, based on file
        name).


    Here are some highlights to understand internal mechanisms and motivations:

    * Let's start by quoting :pep:`3333` (WSGI specification):

          For large files, or for specialized uses of HTTP streaming,
          applications will usually return an iterator (often a
          generator-iterator) that produces the output in a block-by-block
          fashion.

    * `Django WSGI handler (application implementation) return response object
      <https://github.com/django/django/blob/fd1279a44df3b9a837453cd79fd0fbcf81bae39d/django/core/handlers/wsgi.py#L268>`_.

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
                 status=200, content_type=None):
        """Constructor."""
        self.file = file_instance
        super(DownloadResponse, self).__init__(streaming_content=self.file,
                                               status=status,
                                               content_type=content_type)
        self.basename = basename
        self.attachment = attachment
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
            try:
                headers['Content-Length'] = self.file.size
            except (AttributeError, NotImplementedError):
                pass  # Generated files.
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


class ProxiedDownloadResponse(HttpResponse):
    """Base class for internal redirect download responses.

    This base class makes it possible to identify several types of specific
    responses such as
    :py:class:`~django_downloadview.nginx.response.XAccelRedirectResponse`.

    """
