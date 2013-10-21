# -*- coding: utf-8 -*-
"""Port of django-sendfile in django-downloadview."""
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_downloadview.views.storage import StorageDownloadView


def sendfile(request, filename, attachment=False, attachment_filename=None,
             mimetype=None, encoding=None):
    """Port of django-sendfile's API in django-downloadview.

    Instantiates a :class:`~django.core.files.storage.FileSystemStorage` with
    ``settings.SENDFILE_ROOT`` as root folder. Then uses
    :class:`StorageDownloadView` to stream the file by ``filename``.

    """
    storage = FileSystemStorage(location=settings.SENDFILE_ROOT)
    view = StorageDownloadView().as_view(storage=storage,
                                         path=filename,
                                         attachment=attachment,
                                         basename=attachment_filename)
    return view(request)
