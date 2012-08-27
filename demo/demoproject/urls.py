from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^download/', include('demoproject.download.urls')),
)
