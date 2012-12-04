"""django-downloadview provides generic download views for Django."""
from django_downloadview.views import DownloadView, ObjectDownloadView


pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('django-downloadview')

#: Module version, as defined in PEP-0396.
__version__ = distribution.version
