from django.conf.urls import patterns, url

from demoproject.object import views


urlpatterns = patterns(
    '',
    url(r'^default-file/(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.default_file_view,
        name='default_file'),
    url(r'^another-file/(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.another_file_view,
        name='another_file'),
    url(r'^deserialized_basename/(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.deserialized_basename_view,
        name='deserialized_basename'),
    url(r'^inline-file/(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.inline_file_view,
        name='inline_file'),
)
