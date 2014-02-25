# -*- coding: utf-8 -*-
"""Utility functions that may be implemented in external packages."""
import re


charset_pattern = re.compile(r'charset=(?P<charset>.+)$', re.I | re.U)


def content_type_to_charset(content_type):
    """Return charset part of content-type header.

    >>> from django_downloadview.utils import content_type_to_charset
    >>> content_type_to_charset('text/html; charset=utf-8')
    'utf-8'

    """
    match = re.search(charset_pattern, content_type)
    if match:
        return match.group('charset')


def url_basename(url, content_type):
    """Return best-guess basename from URL and content-type.

    >>> from django_downloadview.utils import url_basename

    If URL contains extension, it is kept as-is.

    >>> print(url_basename(u'/path/to/somefile.rst', 'text/plain'))
    somefile.rst

    """
    return url.split('/')[-1]


def import_member(import_string):
    """Import one member of Python module by path.

    >>> import os.path
    >>> imported = import_member('os.path.supports_unicode_filenames')
    >>> os.path.supports_unicode_filenames is imported
    True

    """
    module_name, factory_name = str(import_string).rsplit('.', 1)
    module = __import__(module_name, globals(), locals(), [factory_name], 0)
    return getattr(module, factory_name)
