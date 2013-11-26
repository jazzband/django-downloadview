# -*- coding: utf-8 -*-
"""Apache's specific responses."""
import os.path

from django_downloadview.response import (ProxiedDownloadResponse,
                                          content_disposition)


class XSendfileResponse(ProxiedDownloadResponse):
    "Delegates serving file to Apache via X-Sendfile header."
    def __init__(self, file_path, content_type, basename=None,
                 attachment=True):
        """Return a HttpResponse with headers for Apache X-Sendfile."""
        super(XSendfileResponse, self).__init__(content_type=content_type)
        if attachment:
            self.basename = basename or os.path.basename(file_path)
            self['Content-Disposition'] = content_disposition(self.basename)
        self['X-Sendfile'] = file_path
