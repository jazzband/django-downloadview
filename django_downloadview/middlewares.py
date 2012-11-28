"""Base material for download middlewares."""
from django_downloadview.response import is_download_response


class BaseDownloadMiddleware(object):
    """Base (abstract) Django middleware that process download responses.

    Subclasses **must** implement ``process_download_response`` method.

    """
    def is_download_response(self, response):
        """Return True if ``response`` can be considered as a file download."""
        return is_download_response(response)

    def process_response(self, request, response):
        """Call ``process_download_response()`` if ``response`` is download."""
        if self.is_download_response(response):
            return self.process_download_response(request, response)
        return response

    def process_download_response(self, request, response):
        """Handle file download response."""
        raise NotImplementedError()
