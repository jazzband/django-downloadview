# -*- coding: utf-8 -*-
"""Declaration of API shortcuts."""
from django_downloadview.io import (BytesIteratorIO,  # NoQA
                                    TextIteratorIO)
from django_downloadview.files import (StorageFile,  # NoQA
                                       VirtualFile,
                                       HTTPFile)
from django_downloadview.response import (DownloadResponse,  # NoQA
                                          ProxiedDownloadResponse)
from django_downloadview.middlewares import (BaseDownloadMiddleware,  # NoQA
                                             DownloadDispatcherMiddleware,
                                             SmartDownloadMiddleware)
from django_downloadview.views import (PathDownloadView,  # NoQA
                                       ObjectDownloadView,
                                       StorageDownloadView,
                                       HTTPDownloadView,
                                       VirtualDownloadView,
                                       BaseDownloadView,
                                       DownloadMixin)
from django_downloadview.shortcuts import sendfile  # NoQA
from django_downloadview.test import (assert_download_response,  # NoQA
                                      setup_view,
                                      temporary_media_root)


# Backward compatibility.
StringIteratorIO = TextIteratorIO
