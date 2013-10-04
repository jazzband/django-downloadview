"""django-downloadview provides generic download views for Django."""
import pkg_resources


#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__.replace('-', '_')) \
                           .version


# API shortcuts.
from django_downloadview.response import DownloadResponse  # NoQA
from django_downloadview.middlewares import (  # NoQA
    BaseDownloadMiddleware,
    DownloadDispatcherMiddleware)
from django_downloadview.nginx import XAccelRedirectMiddleware  # NoQA
from django_downloadview.views import (PathDownloadView,  # NoQA
                                       ObjectDownloadView,  # NoQA
                                       StorageDownloadView,  # NoQA
                                       VirtualDownloadView)  # NoQA
