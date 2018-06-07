from django.conf.urls import include, url
from django.views.generic import TemplateView

from demoproject.urlpatterns import patterns

from distutils.version import StrictVersion
from django.utils.version import get_version

if StrictVersion(get_version()) >= StrictVersion('2.0'):
  def safe_include(arg, namespace=None, app_name=None):
    return include((arg, app_name), namespace=namespace)
else:
  safe_include = include


home = TemplateView.as_view(template_name='home.html')


urlpatterns = patterns(
    '',
    # ObjectDownloadView.
    url(r'^object/', safe_include('demoproject.object.urls',
                             app_name='object',
                             namespace='object')),
    # StorageDownloadView.
    url(r'^storage/', safe_include('demoproject.storage.urls',
                              app_name='storage',
                              namespace='storage')),
    # PathDownloadView.
    url(r'^path/', safe_include('demoproject.path.urls',
                           app_name='path',
                           namespace='path')),
    # HTTPDownloadView.
    url(r'^http/', safe_include('demoproject.http.urls',
                           app_name='http',
                           namespace='http')),
    # VirtualDownloadView.
    url(r'^virtual/', safe_include('demoproject.virtual.urls',
                              app_name='virtual',
                              namespace='virtual')),
    # Nginx optimizations.
    url(r'^nginx/', safe_include('demoproject.nginx.urls',
                            app_name='nginx',
                            namespace='nginx')),
    # Apache optimizations.
    url(r'^apache/', safe_include('demoproject.apache.urls',
                             app_name='apache',
                             namespace='apache')),
    # Lighttpd optimizations.
    url(r'^lighttpd/', safe_include('demoproject.lighttpd.urls',
                               app_name='lighttpd',
                               namespace='lighttpd')),
    # An informative homepage.
    url(r'$', home, name='home')
)
