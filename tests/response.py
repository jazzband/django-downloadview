"""Unit tests around responses."""

import unittest

from django_downloadview.apache.response import (
    XSendfileResponse as ApacheXSendfileResponse,
)
from django_downloadview.lighttpd.response import (
    XSendfileResponse as LighttpdXSendfileResponse,
)
from django_downloadview.nginx.response import (
    XAccelRedirectResponse as NginxResponse,
)
from django_downloadview.response import DownloadResponse


class DownloadResponseTestCase(unittest.TestCase):
    """Tests around :class:`django_downloadviews.response.DownloadResponse`."""

    def test_content_disposition_encoding(self):
        """Content-Disposition header is encoded."""
        response = DownloadResponse(
            "fake file",
            attachment=True,
            basename="espacé .txt",
        )
        headers = response.default_headers
        self.assertIn('filename="espace_.txt"', headers["Content-Disposition"])
        self.assertIn(
            "filename*=UTF-8''espac%C3%A9%20.txt", headers["Content-Disposition"]
        )

    def test_content_disposition_escaping(self):
        """Content-Disposition headers escape special characters."""
        response = DownloadResponse(
            "fake file", attachment=True, basename=r'"malicious\file.exe'
        )
        headers = response.default_headers
        self.assertIn(
            r'filename="\"malicious\\file.exe"', headers["Content-Disposition"]
        )

    def test_content_disposition_inline(self):
        """Content-Disposition header with inline disposition."""
        response = DownloadResponse(
            "fake file",
            attachment=False,
            basename="document.txt",
        )
        headers = response.default_headers
        self.assertEqual(
            headers["Content-Disposition"],
            'inline; filename="document.txt"',
        )

    def test_content_disposition_inline_encoding(self):
        """Content-Disposition header with inline disposition and encoded filename."""
        response = DownloadResponse(
            "fake file",
            attachment=False,
            basename="espacé .txt",
        )
        headers = response.default_headers
        self.assertIn('inline; filename="espace_.txt"', headers["Content-Disposition"])
        self.assertIn(
            "filename*=UTF-8''espac%C3%A9%20.txt", headers["Content-Disposition"]
        )


class ProxiedResponseTestCase(unittest.TestCase):
    """Tests around proxied download responses."""

    def test_apache_inline(self):
        """Apache XSendfileResponse sets inline Content-Disposition."""
        response = ApacheXSendfileResponse(
            "/path/to/file.pdf",
            content_type="application/pdf",
            attachment=False,
        )
        self.assertEqual(
            response["Content-Disposition"],
            'inline; filename="file.pdf"',
        )

    def test_lighttpd_inline(self):
        """Lighttpd XSendfileResponse sets inline Content-Disposition."""
        response = LighttpdXSendfileResponse(
            "/path/to/file.pdf",
            content_type="application/pdf",
            attachment=False,
        )
        self.assertEqual(
            response["Content-Disposition"],
            'inline; filename="file.pdf"',
        )

    def test_nginx_inline(self):
        """Nginx XAccelRedirectResponse sets inline Content-Disposition."""
        response = NginxResponse(
            "/protected/file.pdf",
            content_type="application/pdf",
            attachment=False,
        )
        self.assertEqual(
            response["Content-Disposition"],
            'inline; filename="file.pdf"',
        )
