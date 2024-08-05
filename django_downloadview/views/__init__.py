"""Views to stream files."""

# API shortcuts.
from django_downloadview.views.base import BaseDownloadView, DownloadMixin  # NoQA
from django_downloadview.views.http import HTTPDownloadView  # NoQA
from django_downloadview.views.object import ObjectDownloadView  # NoQA
from django_downloadview.views.path import PathDownloadView  # NoQA
from django_downloadview.views.storage import StorageDownloadView  # NoQA
from django_downloadview.views.virtual import VirtualDownloadView  # NoQA
