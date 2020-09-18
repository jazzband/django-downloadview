from django.urls import re_path

from demoproject.object import views

app_name = "object"
urlpatterns = [
    re_path(
        r"^default-file/(?P<slug>[a-zA-Z0-9_-]+)/$",
        views.default_file_view,
        name="default_file",
    ),
    re_path(
        r"^another-file/(?P<slug>[a-zA-Z0-9_-]+)/$",
        views.another_file_view,
        name="another_file",
    ),
    re_path(
        r"^deserialized_basename/(?P<slug>[a-zA-Z0-9_-]+)/$",
        views.deserialized_basename_view,
        name="deserialized_basename",
    ),
    re_path(
        r"^inline-file/(?P<slug>[a-zA-Z0-9_-]+)/$",
        views.inline_file_view,
        name="inline_file",
    ),
]
