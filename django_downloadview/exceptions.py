# -*- coding: utf-8 -*-
"""Custom exceptions."""


class FileNotFound(IOError):
    """Requested file does not exist.

    This exception is to be raised when operations (such as read) fail because
    file does not exist (whatever the storage or location).

    """
