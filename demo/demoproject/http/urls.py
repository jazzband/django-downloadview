from django.urls import path

from demoproject.http import views

app_name = "http"
urlpatterns = [
    path("simple_url/", views.simple_url, name="simple_url"),
    path("avatar_url/", views.avatar_url, name="avatar_url"),
]
