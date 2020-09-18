from django.urls import re_path

from demoproject.storage import views

app_name = "storage"
urlpatterns = [
    re_path(
        r"^static-path/(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$",
        views.static_path,
        name="static_path",
    ),
    re_path(
        r"^dynamic-path/(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$",
        views.dynamic_path,
        name="dynamic_path",
    ),
]
