import django.test
from django.urls import reverse

from django_downloadview import assert_download_response


class StaticPathTestCase(django.test.TestCase):
    def test_download_response(self):
        """'static_path' serves 'fixtures/hello-world.txt'."""
        url = reverse("path:static_path")
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )


class DynamicPathTestCase(django.test.TestCase):
    def test_download_response(self):
        """'dynamic_path' serves 'fixtures/{path}'."""
        url = reverse("path:dynamic_path", kwargs={"path": "hello-world.txt"})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )
