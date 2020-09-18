import os

from django.core.files.base import ContentFile
import django.test
from django.urls import reverse

from django_downloadview.nginx import assert_x_accel_redirect

from demoproject.nginx.views import storage, storage_dir


def setup_file():
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    storage.save("hello-world.txt", ContentFile("Hello world!\n"))


class OptimizedByMiddlewareTestCase(django.test.TestCase):
    def test_response(self):
        """'nginx:optimized_by_middleware' returns X-Accel response."""
        setup_file()
        url = reverse("nginx:optimized_by_middleware")
        response = self.client.get(url)
        assert_x_accel_redirect(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            charset="utf-8",
            basename="hello-world.txt",
            redirect_url="/nginx-optimized-by-middleware/hello-world.txt",
            expires=None,
            with_buffering=None,
            limit_rate=None,
        )


class OptimizedByDecoratorTestCase(django.test.TestCase):
    def test_response(self):
        """'nginx:optimized_by_decorator' returns X-Accel response."""
        setup_file()
        url = reverse("nginx:optimized_by_decorator")
        response = self.client.get(url)
        assert_x_accel_redirect(
            self,
            response,
            content_type="text/plain; charset=utf-8",
            charset="utf-8",
            basename="hello-world.txt",
            redirect_url="/nginx-optimized-by-decorator/hello-world.txt",
            expires=None,
            with_buffering=None,
            limit_rate=None,
        )
