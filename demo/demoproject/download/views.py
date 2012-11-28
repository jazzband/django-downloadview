from os.path import abspath, dirname, join

from django_downloadview import DownloadView, ObjectDownloadView
from django_downloadview.nginx import x_accel_redirect

from demoproject.download.models import Document


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')
hello_world_file = join(fixtures_dir, 'hello-world.txt')


download_hello_world = DownloadView.as_view(filename=hello_world_file,
                                            storage=None)

download_document = ObjectDownloadView.as_view(model=Document)

download_document_nginx = x_accel_redirect(download_document,
                                           media_root='/var/www/files',
                                           media_url='/download-optimized')
