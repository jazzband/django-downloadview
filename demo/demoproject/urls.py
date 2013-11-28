from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


home = TemplateView.as_view(template_name='home.html')


urlpatterns = patterns(
    '',
    # ObjectDownloadView.
    url(r'^object/', include('demoproject.object.urls',
                             app_name='object',
                             namespace='object')),
    # StorageDownloadView.
    url(r'^storage/', include('demoproject.storage.urls',
                              app_name='storage',
                              namespace='storage')),
    # PathDownloadView.
    url(r'^path/', include('demoproject.path.urls',
                           app_name='path',
                           namespace='path')),
    # HTTPDownloadView.
    url(r'^http/', include('demoproject.http.urls',
                           app_name='http',
                           namespace='http')),
    # VirtualDownloadView.
    url(r'^virtual/', include('demoproject.virtual.urls',
                              app_name='virtual',
                              namespace='virtual')),
    # Nginx optimizations.
    url(r'^nginx/', include('demoproject.nginx.urls',
                            app_name='nginx',
                            namespace='nginx')),
    # Apache optimizations.
    url(r'^apache/', include('demoproject.apache.urls',
                             app_name='apache',
                             namespace='apache')),
    # Lighttpd optimizations.
    url(r'^lighttpd/', include('demoproject.lighttpd.urls',
                               app_name='lighttpd',
                               namespace='lighttpd')),
    # An informative homepage.
    url(r'$', home, name='home')
)
