# coding=utf8
"""Test suite for demoproject.download."""
from os import listdir
from os.path import abspath, dirname, join

from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_downloadview.test import temporary_media_root

from demoproject.download.models import Document


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')


class DownloadTestCase(TestCase):
    """Base class for download tests."""
    def setUp(self):
        """Common setup."""
        super(DownloadTestCase, self).setUp()
        self.files = {}
        for f in listdir(fixtures_dir):
            self.files[f] = abspath(join(fixtures_dir, f))

    def assertDownloadHelloWorld(self, response, is_attachment=True):
        """Assert response is 'hello-world.txt' download."""
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'],
                          'text/plain; charset=utf-8')
        self.assertFalse('ContentEncoding' in response)
        if is_attachment:
            self.assertEquals(response['Content-Disposition'],
                              'attachment; filename=hello-world.txt')
        else:
            self.assertFalse('Content-Disposition' in response)
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         ''.join(response.streaming_content))


class PathDownloadViewTestCase(DownloadTestCase):
    """Test "hello_world" and "hello_world_inline" views."""
    def test_download_hello_world(self):
        """hello_world view returns hello-world.txt as attachement."""
        download_url = reverse('hello_world')
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)

    def test_download_hello_world_inline(self):
        """hello_world view returns hello-world.txt as attachement."""
        download_url = reverse('hello_world_inline')
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response, is_attachment=False)


class CustomPathDownloadViewTestCase(DownloadTestCase):
    """Test "fixture_from_path" view."""
    def test_download_hello_world(self):
        """fixture_from_path view returns hello-world.txt as attachement."""
        download_url = reverse('fixture_from_path', args=['hello-world.txt'])
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)


class StorageDownloadViewTestCase(DownloadTestCase):
    """Test "fixture_from_storage" view."""
    def test_download_hello_world(self):
        """fixture_from_storage view returns hello-world.txt as attachement."""
        download_url = reverse('fixture_from_storage',
                               args=['hello-world.txt'])
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)


class ObjectDownloadViewTestCase(DownloadTestCase):
    """Test generic ObjectDownloadView."""
    @temporary_media_root()
    def test_download_hello_world(self):
        """'download_document' view returns hello-world.txt as attachement."""
        slug = 'hello-world'
        download_url = reverse('document', kwargs={'slug': slug})
        Document.objects.create(slug=slug,
                                file=File(open(self.files['hello-world.txt'])))
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)


class GeneratedDownloadViewTestCase(DownloadTestCase):
    """Test "generated_hello_world" view."""
    def test_download_hello_world(self):
        """generated_hello_world view returns hello-world.txt as attachement.

        """
        download_url = reverse('generated_hello_world')
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)


class ProxiedDownloadViewTestCase(DownloadTestCase):
    """Test "http_hello_world" view."""
    def test_download_readme(self):
        """http_hello_world view proxies file from URL."""
        download_url = reverse('http_hello_world')
        response = self.client.get(download_url)
        self.assertDownloadHelloWorld(response)
