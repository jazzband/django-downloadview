# -*- coding: utf-8 -*-
"""Decorators to apply Nginx X-Accel on a specific view."""
from django_downloadview.decorators import DownloadDecorator
from django_downloadview.nginx.middlewares import XAccelRedirectMiddleware


#: Apply BaseXAccelRedirectMiddleware to ``view_func`` response.
#:
#: Proxies additional arguments (``*args``, ``**kwargs``) to
#: :py:class:`BaseXAccelRedirectMiddleware` constructor (``expires``,
#: ``with_buffering``, and ``limit_rate``).
x_accel_redirect = DownloadDecorator(XAccelRedirectMiddleware)
