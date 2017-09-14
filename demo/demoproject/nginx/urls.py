"""URL mapping."""

from django.conf.urls import url

from demoproject.nginx import views
from demoproject.urlpatterns import patterns


urlpatterns = patterns(
    'demoproject.nginx.views',
    url(r'^optimized-by-middleware/$',
        views.optimized_by_middleware,
        name='optimized_by_middleware'),
    url(r'^optimized-by-decorator/$',
        views.optimized_by_decorator,
        name='optimized_by_decorator'),
)
