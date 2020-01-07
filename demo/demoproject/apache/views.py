import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_downloadview import StorageDownloadView
from django_downloadview.apache import x_sendfile

storage_dir = os.path.join(settings.MEDIA_ROOT, "apache")
storage = FileSystemStorage(
    location=storage_dir, base_url="".join([settings.MEDIA_URL, "apache/"])
)


optimized_by_middleware = StorageDownloadView.as_view(
    storage=storage, path="hello-world.txt"
)


optimized_by_decorator = x_sendfile(
    StorageDownloadView.as_view(storage=storage, path="hello-world.txt"),
    source_url=storage.base_url,
    destination_dir="/apache-optimized-by-decorator/",
)
