from django.conf.urls import url

from demoproject.compat import patterns
from demoproject.http import views


urlpatterns = patterns(
    "",
    url(r"^simple_url/$", views.simple_url, name="simple_url"),
    url(r"^avatar_url/$", views.avatar_url, name="avatar_url"),
)
