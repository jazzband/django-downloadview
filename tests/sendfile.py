"""Tests around :py:mod:`django_downloadview.sendfile`."""
from django.http import Http404
import django.test

from django_downloadview.response import DownloadResponse
from django_downloadview.shortcuts import sendfile


class SendfileTestCase(django.test.TestCase):
    """Tests around :func:`django_downloadview.sendfile.sendfile`."""

    def test_defaults(self):
        """sendfile() takes at least request and filename."""
        request = django.test.RequestFactory().get("/fake-url")
        filename = __file__
        response = sendfile(request, filename)
        self.assertTrue(isinstance(response, DownloadResponse))
        self.assertFalse(response.attachment)

    def test_custom(self):
        """sendfile() accepts various arguments for response tuning."""
        request = django.test.RequestFactory().get("/fake-url")
        filename = __file__
        response = sendfile(
            request,
            filename,
            attachment=True,
            attachment_filename="toto.txt",
            mimetype="test/octet-stream",
            encoding="gzip",
        )
        self.assertTrue(isinstance(response, DownloadResponse))
        self.assertTrue(response.attachment)
        self.assertEqual(response.basename, "toto.txt")
        self.assertEqual(response["Content-Type"], "test/octet-stream; charset=utf-8")
        self.assertEqual(response.get_encoding(), "gzip")

    def test_404(self):
        """sendfile() raises Http404 if file does not exists."""
        request = django.test.RequestFactory().get("/fake-url")
        filename = "i-do-no-exist"
        with self.assertRaises(Http404):
            sendfile(request, filename)
