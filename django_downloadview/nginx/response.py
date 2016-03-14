# -*- coding: utf-8 -*-
"""Nginx's specific responses."""
from datetime import timedelta

from django.utils.timezone import now

from django_downloadview.response import (ProxiedDownloadResponse,
                                          content_disposition)
from django_downloadview.utils import content_type_to_charset, url_basename


class XAccelRedirectResponse(ProxiedDownloadResponse):
    "Http response that delegates serving file to Nginx via X-Accel headers."
    def __init__(self, redirect_url, content_type, basename=None, expires=None,
                 with_buffering=None, limit_rate=None, attachment=True):
        """Return a HttpResponse with headers for Nginx X-Accel-Redirect."""
        super(XAccelRedirectResponse, self).__init__(content_type=content_type)
        if attachment:
            self.basename = basename or url_basename(redirect_url,
                                                     content_type)
            self['Content-Disposition'] = content_disposition(self.basename)
        self['X-Accel-Redirect'] = redirect_url
        self['X-Accel-Charset'] = content_type_to_charset(content_type)
        if with_buffering is not None:
            self['X-Accel-Buffering'] = with_buffering and 'yes' or 'no'
        if expires:
            expire_seconds = timedelta(expires - now()).seconds
            self['X-Accel-Expires'] = expire_seconds
        elif expires is not None:  # We explicitely want it off.
            self['X-Accel-Expires'] = 'off'
        if limit_rate is not None:
            self['X-Accel-Limit-Rate'] = \
                limit_rate and '%d' % limit_rate or 'off'
