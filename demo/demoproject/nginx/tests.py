"""Test suite for demoproject.nginx."""
from django.core.files import File
from django.core.urlresolvers import reverse_lazy as reverse

from django_downloadview.nginx import assert_x_accel_redirect
from django_downloadview.test import temporary_media_root

from demoproject.download.models import Document
from demoproject.download.tests import DownloadTestCase


class XAccelRedirectDecoratorTestCase(DownloadTestCase):
    @temporary_media_root()
    def test_response(self):
        """'download_document_nginx' view returns a valid X-Accel response."""
        document = Document.objects.create(
            slug='hello-world',
            file=File(open(self.files['hello-world.txt'])),
        )
        download_url = reverse('download_document_nginx',
                               kwargs={'slug': 'hello-world'})
        response = self.client.get(download_url)
        self.assertEquals(response.status_code, 200)
        # Validation shortcut: assert_x_accel_redirect.
        assert_x_accel_redirect(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            charset="utf-8",
            basename="hello-world.txt",
            redirect_url="/download-optimized/document/hello-world.txt",
            expires=None,
            with_buffering=None,
            limit_rate=None)
        # Check some more items, because this test is part of
        # django-downloadview tests.
        self.assertFalse('ContentEncoding' in response)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename=hello-world.txt')


class InlineXAccelRedirectTestCase(DownloadTestCase):
    @temporary_media_root()
    def test_response(self):
        """X-Accel optimization respects ``attachment`` attribute."""
        document = Document.objects.create(
            slug='hello-world',
            file=File(open(self.files['hello-world.txt'])),
        )
        download_url = reverse('download_document_nginx_inline',
                               kwargs={'slug': 'hello-world'})
        response = self.client.get(download_url)
        assert_x_accel_redirect(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            charset="utf-8",
            attachment=False,
            redirect_url="/download-optimized/document/hello-world.txt",
            expires=None,
            with_buffering=None,
            limit_rate=None)
