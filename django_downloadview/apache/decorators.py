"""Decorators to apply Apache X-Sendfile on a specific view."""

from django_downloadview.apache.middlewares import XSendfileMiddleware
from django_downloadview.decorators import DownloadDecorator


def x_sendfile(view_func, *args, **kwargs):
    """Apply
    :class:`~django_downloadview.apache.middlewares.XSendfileMiddleware` to
    ``view_func``.

    Proxies (``*args``, ``**kwargs``) to middleware constructor.

    """
    decorator = DownloadDecorator(XSendfileMiddleware)
    return decorator(view_func, *args, **kwargs)
