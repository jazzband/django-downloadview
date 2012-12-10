from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


home = TemplateView.as_view(template_name='home.html')


urlpatterns = patterns('',
    # Standard download views.
    url(r'^download/', include('demoproject.download.urls')),
    # Nginx optimizations.
    url(r'^nginx/', include('demoproject.nginx.urls')),
    # An informative page.
    url(r'', home, name='home')
)
