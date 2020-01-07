from distutils.version import StrictVersion
from django.utils.version import get_version


try:
    from django.conf.urls import patterns  # noqa
except ImportError:

    def patterns(prefix, *args):
        return list(args)


try:
    from django.urls import reverse  # noqa
except ImportError:
    from django.core.urlresolvers import reverse  # noqa

if StrictVersion(get_version()) >= StrictVersion("2.0"):
    from django.conf.urls import include as urlinclude  # noqa

    def include(arg, namespace=None, app_name=None):
        return urlinclude((arg, app_name), namespace=namespace)


else:
    from django.conf.urls import include  # noqa
