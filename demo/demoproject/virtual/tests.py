import django.test
from django.urls import reverse

from django_downloadview import assert_download_response


class TextTestCase(django.test.TestCase):
    def test_download_response(self):
        """'virtual:text' serves 'hello-world.txt' from unicode."""
        url = reverse("virtual:text")
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )


class StringIOTestCase(django.test.TestCase):
    def test_download_response(self):
        """'virtual:stringio' serves 'hello-world.txt' from stringio."""
        url = reverse("virtual:stringio")
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )


class GeneratedTestCase(django.test.TestCase):
    def test_download_response(self):
        """'virtual:generated' serves 'hello-world.txt' from generator."""
        url = reverse("virtual:generated")
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content="Hello world!\n",
            basename="hello-world.txt",
            mime_type="text/plain",
        )
