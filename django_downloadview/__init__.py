"""Serve files with Django and reverse proxies."""
import pkg_resources

from django_downloadview.api import *  # NoQA

#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__.replace("-", "_")).version
