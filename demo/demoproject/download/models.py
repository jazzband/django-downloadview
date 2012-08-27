from django.db import models
from django.utils.translation import ugettext_lazy as _


class Document(models.Model):
    """A sample model with a FileField."""
    slug = models.SlugField(verbose_name=_('slug'))
    file = models.FileField(verbose_name=_('file'), upload_to='document')
