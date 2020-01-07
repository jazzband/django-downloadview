from django.db import models


class Document(models.Model):
    slug = models.SlugField()
    file = models.FileField(upload_to="object")
    another_file = models.FileField(upload_to="object-other")
    basename = models.CharField(max_length=100)
