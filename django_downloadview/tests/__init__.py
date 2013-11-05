# -*- coding: utf-8 -*-
"""Unit tests."""


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    ``args`` and ``kwargs`` are the same you would pass to
    :func:`~django.core.urlresolvers.reverse`.

    This is an early implementation of
    https://code.djangoproject.com/ticket/20456

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
