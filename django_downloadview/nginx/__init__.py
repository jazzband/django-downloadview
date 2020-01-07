"""Optimizations for Nginx.

See also `Nginx X-accel documentation <http://wiki.nginx.org/X-accel>`_ and
:doc:`narrative documentation about Nginx optimizations
</optimizations/nginx>`.

"""
# API shortcuts.
from django_downloadview.nginx.decorators import x_accel_redirect  # NoQA
from django_downloadview.nginx.middlewares import XAccelRedirectMiddleware  # NoQA
from django_downloadview.nginx.response import XAccelRedirectResponse  # NoQA
from django_downloadview.nginx.tests import assert_x_accel_redirect  # NoQA
