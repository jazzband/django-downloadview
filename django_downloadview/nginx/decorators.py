# -*- coding: utf-8 -*-
"""Decorators to apply Nginx X-Accel on a specific view."""
from django_downloadview.decorators import DownloadDecorator
from django_downloadview.nginx.middlewares import XAccelRedirectMiddleware


def x_accel_redirect(view_func, *args, **kwargs):
    """Apply
    :class:`~django_downloadview.nginx.middlewares.XAccelRedirectMiddleware` to
    ``view_func``.

    Proxies (``*args``, ``**kwargs``) to middleware constructor.

    """
    decorator = DownloadDecorator(XAccelRedirectMiddleware)
    return decorator(view_func, *args, **kwargs)
