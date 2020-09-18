import django.test
from django.urls import reverse

from django_downloadview import assert_download_response


class SimpleURLTestCase(django.test.TestCase):
    def test_download_response(self):
        """'simple_url' serves 'hello-world.txt' from Github."""
        url = reverse("http:simple_url")
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )


class AvatarTestCase(django.test.TestCase):
    def test_download_response(self):
        """HTTPDownloadView proxies Content-Type header."""
        url = reverse("http:avatar_url")
        response = self.client.get(url)
        assert_download_response(self, response, mime_type="image/png")
