try:
    from django.conf.urls import patterns
except:
    def patterns(prefix, *args):
        return list(args)
