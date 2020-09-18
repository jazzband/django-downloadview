from django.urls import path, re_path

from demoproject.path import views

app_name = "path"
urlpatterns = [
    path("static-path/", views.static_path, name="static_path"),
    re_path(
        r"^dynamic-path/(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$",
        views.dynamic_path,
        name="dynamic_path",
    ),
]
