# -*- coding: utf-8 -*-
"""Stream files given an URL, i.e. files you want to proxy."""
import requests

from django_downloadview.files import HTTPFile
from django_downloadview.views.base import BaseDownloadView


class HTTPDownloadView(BaseDownloadView):
    """Proxy files that live on remote servers."""
    #: URL to download (the one we are proxying).
    url = u''

    #: Additional keyword arguments for request handler.
    request_kwargs = {}

    def get_request_factory(self):
        """Return request factory to perform actual HTTP request.

        Default implementation returns :func:`requests.get` callable.

        """
        return requests.get

    def get_request_kwargs(self):
        """Return keyword arguments for use with :meth:`get_request_factory`.

        Default implementation returns :attr:`request_kwargs`.

        """
        return self.request_kwargs

    def get_url(self):
        """Return remote file URL (the one we are proxying).

        Default implementation returns :attr:`url`.

        """
        return self.url

    def get_file(self):
        """Return wrapper which has an ``url`` attribute."""
        return HTTPFile(request_factory=self.get_request_factory(),
                        name=self.get_basename(),
                        url=self.get_url(),
                        **self.get_request_kwargs())
