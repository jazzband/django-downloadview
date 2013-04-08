"""URL mapping."""
from django.conf.urls import patterns, url


urlpatterns = patterns('demoproject.nginx.views',
    url(r'^document-nginx/(?P<slug>[a-zA-Z0-9_-]+)/$',
        'download_document_nginx', name='download_document_nginx'),
)
