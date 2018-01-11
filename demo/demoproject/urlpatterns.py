try:
    from django.conf.urls import patterns
except ImportError:
    def patterns(prefix, *args):
        return list(args)
