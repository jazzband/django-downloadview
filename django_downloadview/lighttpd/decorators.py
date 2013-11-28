# -*- coding: utf-8 -*-
"""Decorators to apply Lighttpd X-Sendfile on a specific view."""
from django_downloadview.decorators import DownloadDecorator
from django_downloadview.lighttpd.middlewares import XSendfileMiddleware


def x_sendfile(view_func, *args, **kwargs):
    """Apply
    :class:`~django_downloadview.lighttpd.middlewares.XSendfileMiddleware` to
    ``view_func``.

    Proxies (``*args``, ``**kwargs``) to middleware constructor.

    """
    decorator = DownloadDecorator(XSendfileMiddleware)
    return decorator(view_func, *args, **kwargs)
