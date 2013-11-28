# -*- coding: utf-8 -*-
"""Port of django-sendfile in django-downloadview."""
from django_downloadview.views.path import PathDownloadView


def sendfile(request, filename, attachment=False, attachment_filename=None,
             mimetype=None, encoding=None):
    """Port of django-sendfile's API in django-downloadview.

    Instantiates a :class:`~django.core.files.storage.FileSystemStorage` with
    ``settings.SENDFILE_ROOT`` as root folder. Then uses
    :class:`StorageDownloadView` to stream the file by ``filename``.

    """
    view = PathDownloadView().as_view(path=filename,
                                      attachment=attachment,
                                      basename=attachment_filename)
    return view(request)
