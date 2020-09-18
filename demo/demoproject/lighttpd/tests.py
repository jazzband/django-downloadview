import os

from django.core.files.base import ContentFile
import django.test
from django.urls import reverse

from django_downloadview.lighttpd import assert_x_sendfile

from demoproject.lighttpd.views import storage, storage_dir


def setup_file():
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    storage.save("hello-world.txt", ContentFile("Hello world!\n"))


class OptimizedByMiddlewareTestCase(django.test.TestCase):
    def test_response(self):
        """'lighttpd:optimized_by_middleware' returns X-Sendfile response."""
        setup_file()
        url = reverse("lighttpd:optimized_by_middleware")
        response = self.client.get(url)
        assert_x_sendfile(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            basename="hello-world.txt",
            file_path="/lighttpd-optimized-by-middleware/hello-world.txt",
        )


class OptimizedByDecoratorTestCase(django.test.TestCase):
    def test_response(self):
        """'lighttpd:optimized_by_decorator' returns X-Sendfile response."""
        setup_file()
        url = reverse("lighttpd:optimized_by_decorator")
        response = self.client.get(url)
        assert_x_sendfile(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            basename="hello-world.txt",
            file_path="/lighttpd-optimized-by-decorator/hello-world.txt",
        )
