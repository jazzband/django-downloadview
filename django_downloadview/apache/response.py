"""Apache's specific responses."""

import os.path

from django_downloadview.response import ProxiedDownloadResponse, content_disposition


class XSendfileResponse(ProxiedDownloadResponse):
    "Delegates serving file to Apache via X-Sendfile header."

    def __init__(
        self, file_path, content_type, basename=None, attachment=True, headers=None
    ):
        """Return a HttpResponse with headers for Apache X-Sendfile."""
        # content-type must be provided only as keyword argument to response
        if headers and content_type:
            headers.pop("Content-Type", None)
        super().__init__(content_type=content_type, headers=headers)
        if attachment:
            self.basename = basename or os.path.basename(file_path)
            self["Content-Disposition"] = content_disposition(self.basename)
        self["X-Sendfile"] = file_path
