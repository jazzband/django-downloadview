from os.path import abspath, dirname, join

from django_downloadview import DownloadView


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')
hello_world_file = join(fixtures_dir, 'hello-world.txt')


download_hello_world = DownloadView.as_view(file=hello_world_file)
