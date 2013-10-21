# -*- coding: utf-8 -*-
"""Declaration of API shortcuts."""
from django_downloadview.io import StringIteratorIO  # NoQA
from django_downloadview.files import (StorageFile,  # NoQA
                                       VirtualFile,
                                       HTTPFile)
from django_downloadview.response import (DownloadResponse,  # NoQA
                                          ProxiedDownloadResponse)
from django_downloadview.middlewares import (BaseDownloadMiddleware,  # NoQA
                                             DownloadDispatcherMiddleware)
from django_downloadview.nginx import XAccelRedirectMiddleware  # NoQA
from django_downloadview.views import (PathDownloadView,  # NoQA
                                       ObjectDownloadView,
                                       StorageDownloadView,
                                       VirtualDownloadView)
from django_downloadview.sendfile import sendfile  # NoQA
