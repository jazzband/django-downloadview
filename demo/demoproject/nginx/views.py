"""Views."""
from django.conf import settings

from django_downloadview.nginx import x_accel_redirect

from demoproject.download import views


download_document_nginx = x_accel_redirect(
    views.download_document,
    source_dir='/var/www/files',
    destination_url='/download-optimized')


download_document_nginx_inline = x_accel_redirect(
    views.download_document_inline,
    source_dir=settings.MEDIA_ROOT,
    destination_url='/download-optimized')
