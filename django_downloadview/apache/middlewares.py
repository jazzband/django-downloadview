from django_downloadview.apache.response import XSendfileResponse
from django_downloadview.middlewares import (ProxiedDownloadMiddleware,
                                             NoRedirectionMatch)


class XSendfileMiddleware(ProxiedDownloadMiddleware):
    """Configurable middleware, for use in decorators or in global middlewares.

    Standard Django middlewares are configured globally via settings. Instances
    of this class are to be configured individually. It makes it possible to
    use this class as the factory in
    :py:class:`django_downloadview.decorators.DownloadDecorator`.

    """
    def __init__(self, source_dir=None, source_url=None, destination_dir=None):
        """Constructor."""
        super(XSendfileMiddleware, self).__init__(source_dir,
                                                  source_url,
                                                  destination_dir)

    def process_download_response(self, request, response):
        """Replace DownloadResponse instances by XSendfileResponse ones."""
        try:
            redirect_url = self.get_redirect_url(response)
        except NoRedirectionMatch:
            return response
        return XSendfileResponse(file_path=redirect_url,
                                 content_type=response['Content-Type'],
                                 basename=response.basename,
                                 attachment=response.attachment)
