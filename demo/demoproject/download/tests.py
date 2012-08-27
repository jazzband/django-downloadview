"""Test suite for django-downloadview."""
from os import listdir
from os.path import abspath, dirname, join

from django.core.urlresolvers import reverse
from django.test import TestCase


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')


class DownloadViewTestCase(TestCase):
    """Test generic DownloadView."""
    def setUp(self):
        """Common setup."""
        super(DownloadViewTestCase, self).setUp()
        self.download_hello_world_url = reverse('download_hello_world')
        self.files = {}
        for f in listdir(fixtures_dir):
            self.files[f] = abspath(join(fixtures_dir, f))

    def test_download_hello_world(self):
        """Download_hello_world view returns hello-world.txt as attachement."""
        response = self.client.get(self.download_hello_world_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/octet-stream')
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         response.content) 
