"""Test suite for django-downloadview."""
from os import listdir
from os.path import abspath, dirname, join

from django.core.files import File
from django.core.urlresolvers import reverse_lazy as reverse
from django.test import TestCase

from demoproject.download.models import Document


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')


class DownloadTestCase(TestCase):
    """Base class for download tests."""
    def setUp(self):
        """Common setup."""
        super(DownloadTestCase, self).setUp()
        self.download_hello_world_url = reverse('download_hello_world')
        self.download_document_url = reverse('download_document',
                                             kwargs={'slug': 'hello-world'})
        self.files = {}
        for f in listdir(fixtures_dir):
            self.files[f] = abspath(join(fixtures_dir, f))


class DownloadViewTestCase(DownloadTestCase):
    """Test generic DownloadView."""
    def test_download_hello_world(self):
        """Download_hello_world view returns hello-world.txt as attachement."""
        response = self.client.get(self.download_hello_world_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/octet-stream')
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         response.content) 


class ObjectDownloadViewTestCase(DownloadTestCase):
    """Test generic ObjectDownloadView."""
    def test_download_hello_world(self):
        """Download_hello_world view returns hello-world.txt as attachement."""
        document = Document.objects.create(
            slug='hello-world',
            file=File(open(self.files['hello-world.txt'])),
        )
        response = self.client.get(self.download_document_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/octet-stream')
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         response.content) 
