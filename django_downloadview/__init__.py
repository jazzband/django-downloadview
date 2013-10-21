# -*- coding: utf-8 -*-
"""django-downloadview provides generic download views for Django."""
import pkg_resources


#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__.replace('-', '_')) \
                           .version


# API shortcuts.
from django_downloadview.api import *  # NoQA
