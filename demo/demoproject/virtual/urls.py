from django.urls import path

from demoproject.virtual import views

app_name = "virtual"
urlpatterns = [
    path("text/", views.TextDownloadView.as_view(), name="text"),
    path("stringio/", views.StringIODownloadView.as_view(), name="stringio"),
    path("gerenated/", views.GeneratedDownloadView.as_view(), name="generated"),
]
