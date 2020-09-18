"""URL mapping."""
from django.urls import path

from demoproject.lighttpd import views

app_name = "lighttpd"
urlpatterns = [
    path(
        "optimized-by-middleware/",
        views.optimized_by_middleware,
        name="optimized_by_middleware",
    ),
    path(
        "optimized-by-decorator/",
        views.optimized_by_decorator,
        name="optimized_by_decorator",
    ),
]
