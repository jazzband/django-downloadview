from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


home = TemplateView.as_view(template_name='home.html')


urlpatterns = patterns('',
    url(r'^download/', include('demoproject.download.urls')),
    url(r'', home, name='home')
)
