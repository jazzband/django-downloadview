"""Views."""
from django_downloadview.nginx import x_accel_redirect

from demoproject.download.views import download_document


download_document_nginx = x_accel_redirect(download_document,
                                           media_root='/var/www/files',
                                           media_url='/download-optimized')
