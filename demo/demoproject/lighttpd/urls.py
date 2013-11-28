"""URL mapping."""
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'demoproject.lighttpd.views',
    url(r'^optimized-by-middleware/$',
        'optimized_by_middleware',
        name='optimized_by_middleware'),
    url(r'^optimized-by-decorator/$',
        'optimized_by_decorator',
        name='optimized_by_decorator'),
)
