"""URL mapping."""
from django.conf.urls import url

from demoproject.compat import patterns
from demoproject.lighttpd import views


urlpatterns = patterns(
    "demoproject.lighttpd.views",
    url(
        r"^optimized-by-middleware/$",
        views.optimized_by_middleware,
        name="optimized_by_middleware",
    ),
    url(
        r"^optimized-by-decorator/$",
        views.optimized_by_decorator,
        name="optimized_by_decorator",
    ),
)
