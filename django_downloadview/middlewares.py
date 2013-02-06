"""Base material for download middlewares."""
from django_downloadview.response import is_download_response


class BaseDownloadMiddleware(object):
    """Base (abstract) Django middleware that handles download responses.

    Subclasses **must** implement :py:meth:`process_download_response` method.

    """
    def is_download_response(self, response):
        """Return True if ``response`` can be considered as a file download.

        By default, this method uses
        :py:func:`django_downloadview.response.is_download_response`.
        Override this method if you want a different behaviour.

        """
        return is_download_response(response)

    def process_response(self, request, response):
        """Call :py:meth:`process_download_response` if ``response`` is download."""
        if self.is_download_response(response):
            return self.process_download_response(request, response)
        return response

    def process_download_response(self, request, response):
        """Handle file download response."""
        raise NotImplementedError()
