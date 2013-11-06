from django.conf.urls import patterns, url

from demoproject.virtual import views


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
