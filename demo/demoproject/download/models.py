from django.db import models


class Document(models.Model):
    """A sample model with a FileField."""
    slug = models.SlugField(verbose_name='slug')
    file = models.FileField(verbose_name='file', upload_to='document')
