"""URL mapping."""
from django.urls import path

from demoproject.apache import views

app_name = "apache"
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
