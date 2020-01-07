# flake8: noqa
"""Declaration of API shortcuts."""
from django_downloadview.files import HTTPFile, StorageFile, VirtualFile
from django_downloadview.io import BytesIteratorIO, TextIteratorIO
from django_downloadview.middlewares import (
    BaseDownloadMiddleware,
    DownloadDispatcherMiddleware,
    SmartDownloadMiddleware,
)
from django_downloadview.response import DownloadResponse, ProxiedDownloadResponse
from django_downloadview.shortcuts import sendfile
from django_downloadview.test import (
    assert_download_response,
    setup_view,
    temporary_media_root,
)
from django_downloadview.views import (
    BaseDownloadView,
    DownloadMixin,
    HTTPDownloadView,
    ObjectDownloadView,
    PathDownloadView,
    StorageDownloadView,
    VirtualDownloadView,
)

# Backward compatibility.
StringIteratorIO = TextIteratorIO
