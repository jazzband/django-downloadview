"""URLconf for tests."""
from django.conf.urls import patterns, include, url


urlpatterns = patterns('demoproject.download.views',
    url(r'^hello-world\.txt$', 'download_hello_world',
        name='download_hello_world'),
    url(r'^document/(?P<slug>[a-zA-Z0-9_-]+)/$', 'download_document',
        name='download_document'),
)
