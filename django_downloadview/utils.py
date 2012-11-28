"""Utility functions."""
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
