###################
django-downloadview
###################

`django-downloadview` makes it easy to serve files with `Django`_:

* you manage files with Django (permissions, filters, generation, ...);

* files are stored somewhere or generated somehow (local filesystem, remote
  storage, memory...);

* `django-downloadview` helps you stream the files with very little code;

* `django-downloadview` helps you improve performances with reverse proxies,
  via mechanisms such as Nginx's X-Accel or Apache's X-Sendfile.


*******
Example
*******

Let's serve a file stored in a file field of some model:

.. code:: python

   from django.conf.urls import url, url_patterns
   from django_downloadview import ObjectDownloadView
   from demoproject.download.models import Document  # A model with a FileField

   # ObjectDownloadView inherits from django.views.generic.BaseDetailView.
   download = ObjectDownloadView.as_view(model=Document, file_field='file')

   url_patterns = ('',
       url('^download/(?P<slug>[A-Za-z0-9_-]+)/$', download, name='download'),
   )


*********
Resources
*********

* Documentation: http://django-downloadview.readthedocs.org
* PyPI page: http://pypi.python.org/pypi/django-downloadview
* Code repository: https://github.com/benoitbryon/django-downloadview
* Bugtracker: https://github.com/benoitbryon/django-downloadview/issues
* Continuous integration: https://travis-ci.org/benoitbryon/django-downloadview
* Roadmap: https://github.com/benoitbryon/django-downloadview/milestones


.. _`Django`: https://djangoproject.com
