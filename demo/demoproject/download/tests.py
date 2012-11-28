"""Test suite for django-downloadview."""
from os import listdir
from os.path import abspath, dirname, join
import shutil
import tempfile

from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse_lazy as reverse
from django.test import TestCase
from django.test.utils import override_settings

from django_downloadview.nginx import XAccelRedirectResponse

from demoproject.download.models import Document


app_dir = dirname(abspath(__file__))
fixtures_dir = join(app_dir, 'fixtures')


class temporary_media_root(override_settings):
    """Context manager or decorator to override settings.MEDIA_ROOT.

    >>> from django.conf import settings
    >>> global_media_root = settings.MEDIA_ROOT
    >>> with temporary_media_root():
    ...     global_media_root == settings.MEDIA_ROOT
    False
    >>> global_media_root == settings.MEDIA_ROOT
    True

    >>> @temporary_media_root
    ... def use_temporary_media_root():
    ...     return settings.MEDIA_ROOT
    >>> tmp_media_root = use_temporary_media_root()
    >>> global_media_root == tmp_media_root
    False
    >>> global_media_root == settings.MEDIA_ROOT
    True

    """
    def enable(self):
        """Create a temporary directory and use it to override
        settings.MEDIA_ROOT."""
        tmp_dir = tempfile.mkdtemp()
        self.options['MEDIA_ROOT'] = tmp_dir
        super(temporary_media_root, self).enable()

    def disable(self):
        """Remove directory settings.MEDIA_ROOT then restore original
        setting."""
        shutil.rmtree(settings.MEDIA_ROOT)
        super(temporary_media_root, self).disable()


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
        self.assertEquals(response['Content-Type'],
                          'text/plain; charset=utf-8')
        self.assertFalse('ContentEncoding' in response)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         response.content)


class ObjectDownloadViewTestCase(DownloadTestCase):
    """Test generic ObjectDownloadView."""
    @temporary_media_root()
    def test_download_hello_world(self):
        """Download_hello_world view returns hello-world.txt as attachement."""
        document = Document.objects.create(
            slug='hello-world',
            file=File(open(self.files['hello-world.txt'])),
        )
        response = self.client.get(self.download_document_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'],
                          'text/plain; charset=utf-8')
        self.assertFalse('ContentEncoding' in response)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEqual(open(self.files['hello-world.txt']).read(),
                         response.content)


class XAccelRedirectDecoratorTestCase(DownloadTestCase):
    @temporary_media_root()
    def test_response(self):
        document = Document.objects.create(
            slug='hello-world',
            file=File(open(self.files['hello-world.txt'])),
        )
        download_url = reverse('download_document_nginx',
                               kwargs={'slug': 'hello-world'})
        response = self.client.get(download_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response, XAccelRedirectResponse))
        self.assertEquals(response['Content-Type'],
                          'text/plain; charset=utf-8')
        self.assertFalse('ContentEncoding' in response)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')
        self.assertEquals(response['X-Accel-Redirect'],
                          '/download-optimized/document/hello-world.txt') 
