from django.conf.urls import url

from demoproject.virtual import views
from demoproject.urlpatterns import patterns


urlpatterns = patterns(
    '',
    url(r'^text/$',
        views.TextDownloadView.as_view(),
        name='text'),
    url(r'^stringio/$',
        views.StringIODownloadView.as_view(),
        name='stringio'),
    url(r'^gerenated/$',
        views.GeneratedDownloadView.as_view(),
        name='generated'),
)
