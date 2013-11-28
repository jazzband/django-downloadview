# -*- coding: utf-8 -*-
"""Optimizations for Apache.

See also `documentation of mod_xsendfile for Apache
<https://tn123.org/mod_xsendfile/>`_ and :doc:`narrative documentation about
Apache optimizations </optimizations/apache>`.

"""
# API shortcuts.
from django_downloadview.apache.decorators import x_sendfile  # NoQA
from django_downloadview.apache.response import XSendfileResponse  # NoQA
from django_downloadview.apache.tests import assert_x_sendfile  # NoQA
from django_downloadview.apache.middlewares import XSendfileMiddleware  # NoQA
