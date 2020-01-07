"""Declaration of API shortcuts."""
from django_downloadview.files import HTTPFile, StorageFile, VirtualFile  # NoQA
from django_downloadview.io import BytesIteratorIO, TextIteratorIO  # NoQA
from django_downloadview.middlewares import BaseDownloadMiddleware  # NoQA
from django_downloadview.middlewares import (
    DownloadDispatcherMiddleware,
    SmartDownloadMiddleware,
)
from django_downloadview.response import DownloadResponse  # NoQA
from django_downloadview.response import ProxiedDownloadResponse
from django_downloadview.shortcuts import sendfile  # NoQA
from django_downloadview.test import assert_download_response  # NoQA
from django_downloadview.test import setup_view, temporary_media_root
from django_downloadview.views import PathDownloadView  # NoQA
from django_downloadview.views import (
    BaseDownloadView,
    DownloadMixin,
    HTTPDownloadView,
    ObjectDownloadView,
    StorageDownloadView,
    VirtualDownloadView,
)

# Backward compatibility.
StringIteratorIO = TextIteratorIO
