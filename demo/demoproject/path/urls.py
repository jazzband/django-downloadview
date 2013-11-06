from django.conf.urls import patterns, url

from demoproject.path import views


urlpatterns = patterns(
    '',
    url(r'^static-path/$',
        views.static_path,
        name='static_path'),
    url(r'^dynamic-path/(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$',
        views.dynamic_path,
        name='dynamic_path'),
)
