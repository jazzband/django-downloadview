from django.conf.urls import patterns, url

from demoproject.http import views


urlpatterns = patterns(
    '',
    url(r'^simple_url/$',
        views.simple_url,
        name='simple_url'),
)
