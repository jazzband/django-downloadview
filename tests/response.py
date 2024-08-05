"""Unit tests around responses."""

import unittest

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
