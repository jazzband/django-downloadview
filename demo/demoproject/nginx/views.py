import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_downloadview import StorageDownloadView
from django_downloadview.nginx import x_accel_redirect

storage_dir = os.path.join(settings.MEDIA_ROOT, "nginx")
storage = FileSystemStorage(
    location=storage_dir, base_url="".join([settings.MEDIA_URL, "nginx/"])
)


optimized_by_middleware = StorageDownloadView.as_view(
    storage=storage, path="hello-world.txt"
)


optimized_by_decorator = x_accel_redirect(
    StorageDownloadView.as_view(storage=storage, path="hello-world.txt"),
    source_url=storage.base_url,
    destination_url="/nginx-optimized-by-decorator/",
)
