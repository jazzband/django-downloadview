# -*- coding: utf-8 -*-
"""Optimizations for Lighttpd.

See also `documentation of X-Sendfile for Lighttpd
<http://redmine.lighttpd.net/projects/lighttpd/wiki/X-LIGHTTPD-send-file>`_ and
:doc:`narrative documentation about Lighttpd optimizations
</optimizations/lighttpd>`.

"""
# API shortcuts.
from django_downloadview.lighttpd.decorators import x_sendfile  # NoQA
from django_downloadview.lighttpd.response import XSendfileResponse  # NoQA
from django_downloadview.lighttpd.tests import assert_x_sendfile  # NoQA
from django_downloadview.lighttpd.middlewares import XSendfileMiddleware  # NoQA
