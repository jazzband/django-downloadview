import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_downloadview import StorageDownloadView
from django_downloadview.lighttpd import x_sendfile

storage_dir = os.path.join(settings.MEDIA_ROOT, "lighttpd")
storage = FileSystemStorage(
    location=storage_dir, base_url="".join([settings.MEDIA_URL, "lighttpd/"])
)


optimized_by_middleware = StorageDownloadView.as_view(
    storage=storage, path="hello-world.txt"
)


optimized_by_decorator = x_sendfile(
    StorageDownloadView.as_view(storage=storage, path="hello-world.txt"),
    source_url=storage.base_url,
    destination_dir="/lighttpd-optimized-by-decorator/",
)


def _modified_headers(request):
    view = StorageDownloadView.as_view(storage=storage, path="hello-world.txt")
    response = view(request)
    response["X-Test"] = "header"
    return response


modified_headers = x_sendfile(
    _modified_headers,
    source_url=storage.base_url,
    destination_dir="/lighttpd-modified-headers/",
)
