import datetime
import unittest

from django.core.files.base import ContentFile
from django.http.response import HttpResponseNotModified
import django.test
from django.urls import reverse

from django_downloadview import (
    assert_download_response,
    setup_view,
    temporary_media_root,
)

from demoproject.storage import views

# Fixtures.
file_content = "Hello world!\n"


def setup_file(path):
    views.storage.save(path, ContentFile(file_content))


class StaticPathTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        """'storage:static_path' streams file by path."""
        setup_file("1.txt")
        url = reverse("storage:static_path", kwargs={"path": "1.txt"})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=file_content,
            basename="1.txt",
            mime_type="text/plain",
        )

    @temporary_media_root()
    def test_not_modified_download_response(self):
        """'storage:static_path' sends not modified response if unmodified."""
        setup_file("1.txt")
        url = reverse("storage:static_path", kwargs={"path": "1.txt"})
        year = datetime.date.today().year + 4
        response = self.client.get(
            url,
            HTTP_IF_MODIFIED_SINCE=f"Sat, 29 Oct {year} 19:43:31 GMT",
        )
        self.assertTrue(isinstance(response, HttpResponseNotModified))

    @temporary_media_root()
    def test_modified_since_download_response(self):
        """'storage:static_path' streams file if modified."""
        setup_file("1.txt")
        url = reverse("storage:static_path", kwargs={"path": "1.txt"})
        response = self.client.get(
            url, HTTP_IF_MODIFIED_SINCE="Sat, 29 Oct 1980 19:43:31 GMT"
        )
        assert_download_response(
            self,
            response,
            content=file_content,
            basename="1.txt",
            mime_type="text/plain",
        )


class DynamicPathIntegrationTestCase(django.test.TestCase):
    """Integration tests around ``storage:dynamic_path`` URL."""

    @temporary_media_root()
    def test_download_response(self):
        """'dynamic_path' streams file by generated path.

        As we use ``self.client``, this test involves the whole Django stack,
        including settings, middlewares, decorators... So we need to setup a
        file, the storage, and an URL.

        This test actually asserts the URL ``storage:dynamic_path`` streams a
        file in storage.

        """
        setup_file("1.TXT")
        url = reverse("storage:dynamic_path", kwargs={"path": "1.txt"})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=file_content,
            basename="1.TXT",
            mime_type="text/plain",
        )


class DynamicPathUnitTestCase(unittest.TestCase):
    """Unit tests around ``views.DynamicStorageDownloadView``."""

    def test_get_path(self):
        """DynamicStorageDownloadView.get_path() returns uppercase path.

        Uses :func:`~django_downloadview.test.setup_view` to target only
        overriden methods.

        This test does not involve URLconf, middlewares or decorators. It is
        fast. It has clear scope. It does not assert ``storage:dynamic_path``
        URL works. It targets only custom ``DynamicStorageDownloadView`` class.

        """
        view = setup_view(
            views.DynamicStorageDownloadView(),
            django.test.RequestFactory().get("/fake-url"),
            path="dummy path",
        )
        path = view.get_path()
        self.assertEqual(path, "DUMMY PATH")
