# -*- coding: utf-8 -*-
"""Stream files that live in models."""
from django.views.generic.detail import SingleObjectMixin

from django_downloadview.views.base import BaseDownloadView


class ObjectDownloadView(SingleObjectMixin, BaseDownloadView):
    """Serve file fields from models.

    This class extends BaseDetailView, so you can use its arguments to target
    the instance to operate on: slug, slug_kwarg, model, queryset...
    See Django's DetailView reference for details.

    In addition to BaseDetailView arguments, you can set arguments related to
    the file to be downloaded.

    The main one is ``file_field``.

    The other arguments are provided for convenience, in case your model holds
    some (deserialized) metadata about the file, such as its basename, its
    modification time, its MIME type... These fields may be particularly handy
    if your file storage is not the local filesystem.

    """
    #: Name of the model's attribute which contains the file to be streamed.
    #: Typically the name of a FileField.
    file_field = 'file'

    #: Optional name of the model's attribute which contains the basename.
    basename_field = None

    #: Optional name of the model's attribute which contains the encoding.
    encoding_field = None

    #: Optional name of the model's attribute which contains the MIME type.
    mime_type_field = None

    #: Optional name of the model's attribute which contains the charset.
    charset_field = None

    #: Optional name of the model's attribute which contains the modification
    # time.
    modification_time_field = None

    #: Optional name of the model's attribute which contains the size.
    size_field = None

    def get_file(self):
        """Return :class:`~django.db.models.fields.files.FieldFile` instance.

        The file wrapper is model's field specified as :attr:`file_field`. It
        is typically a :class:`~django.db.models.fields.files.FieldFile` or
        subclass.

        Additional attributes are set on the file wrapper if :attr:`encoding`,
        :attr:`mime_type`, :attr:`charset`, :attr:`modification_time` or
        :attr:`size` are configured.

        """
        file_instance = getattr(self.object, self.file_field)
        for field in ('encoding', 'mime_type', 'charset', 'modification_time',
                      'size'):
            model_field = getattr(self, '%s_field' % field, False)
            if model_field:
                value = getattr(self.object, model_field)
                setattr(file_instance, field, value)
        return file_instance

    def get_basename(self):
        """Return client-side filename."""
        basename = super(ObjectDownloadView, self).get_basename()
        if basename is None:
            field = 'basename'
            model_field = getattr(self, '%s_field' % field, False)
            if model_field:
                basename = getattr(self.object, model_field)
        return basename

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ObjectDownloadView, self).get(request, *args, **kwargs)
