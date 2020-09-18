from django.urls import include, path
from django.views.generic import TemplateView

home = TemplateView.as_view(template_name="home.html")


urlpatterns = [
    # ObjectDownloadView.
    path(
        "object/",
        include("demoproject.object.urls", namespace="object"),
    ),
    # StorageDownloadView.
    path(
        "storage/",
        include("demoproject.storage.urls", namespace="storage"),
    ),
    # PathDownloadView.
    path("path/", include("demoproject.path.urls", namespace="path")),
    # HTTPDownloadView.
    path("http/", include("demoproject.http.urls", namespace="http")),
    # VirtualDownloadView.
    path(
        "virtual/",
        include("demoproject.virtual.urls", namespace="virtual"),
    ),
    # Nginx optimizations.
    path(
        "nginx/",
        include("demoproject.nginx.urls", namespace="nginx"),
    ),
    # Apache optimizations.
    path(
        "apache/",
        include("demoproject.apache.urls", namespace="apache"),
    ),
    # Lighttpd optimizations.
    path(
        "lighttpd/",
        include("demoproject.lighttpd.urls", namespace="lighttpd"),
    ),
    # An informative homepage.
    path("", home, name="home"),
]
