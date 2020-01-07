
try:
    from django.conf.urls import patterns
except Exception:
    def urlpatterns(prefix, *args):
        return list(args)

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
