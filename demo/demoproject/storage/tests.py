try:
    from unittest import mock
except ImportError:  # Python 2.x fallback.
    import mock

from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
import django.test

from django_downloadview import temporary_media_root, assert_download_response

from demoproject.storage.views import storage


# Fixtures.
file_content = 'Hello world!\n'


def setup_file(path):
    storage.save(path, ContentFile(file_content))


class StaticPathTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        """'static_path' streams file by path."""
        setup_file('1.txt')
        url = reverse('storage:static_path', kwargs={'path': '1.txt'})
        response = self.client.get(url)
        assert_download_response(self,
                                 response,
                                 content=file_content,
                                 basename='1.txt',
                                 mime_type='text/plain')


class DynamicPathTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        """'dynamic_path' streams file by generated path."""
        setup_file('1.TXT')
        url = reverse('storage:dynamic_path', kwargs={'path': '1.txt'})
        response = self.client.get(url)
        assert_download_response(self,
                                 response,
                                 content=file_content,
                                 basename='1.TXT',
                                 mime_type='text/plain')
