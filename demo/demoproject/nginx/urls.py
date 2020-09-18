"""URL mapping."""

from django.urls import path

from demoproject.nginx import views

app_name = "nginx"
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
