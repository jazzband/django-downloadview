"""URLconf for tests."""
from django.conf.urls import patterns, include, url


urlpatterns = patterns('demoproject.download.views',
    url(r'^download/hello-world\.txt$', 'download_hello_world',
        name='download_hello_world'),
)
