from os.path import abspath, dirname, join

from django_downloadview import DownloadView, ObjectDownloadView

from demoproject.download.models import Document


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')
hello_world_file = join(fixtures_dir, 'hello-world.txt')


download_hello_world = DownloadView.as_view(file=hello_world_file)


download_document = ObjectDownloadView.as_view(model=Document)
