###################
django-downloadview
###################

.. image:: https://jazzband.co/static/img/badge.svg
    :target: https://jazzband.co/
    :alt: Jazzband

.. image:: https://img.shields.io/pypi/v/django-downloadview.svg
    :target: https://pypi.python.org/pypi/django-downloadview

.. image:: https://img.shields.io/pypi/pyversions/django-downloadview.svg
    :target: https://pypi.python.org/pypi/django-downloadview

.. image:: https://img.shields.io/pypi/djversions/django-downloadview.svg
    :target: https://pypi.python.org/pypi/django-downloadview

.. image:: https://img.shields.io/pypi/dm/django-downloadview.svg
    :target: https://pypi.python.org/pypi/django-downloadview

.. image:: https://github.com/jazzband/django-downloadview/workflows/Test/badge.svg
    :target: https://github.com/jazzband/django-downloadview/actions
    :alt: GitHub Actions

.. image:: https://codecov.io/gh/jazzband/django-downloadview/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jazzband/django-downloadview
    :alt: Coverage

``django-downloadview`` makes it easy to serve files with `Django`_:

* you manage files with Django (permissions, filters, generation, ...);

* files are stored somewhere or generated somehow (local filesystem, remote
  storage, memory...);

* ``django-downloadview`` helps you stream the files with very little code;

* ``django-downloadview`` helps you improve performances with reverse proxies,
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

* Documentation: https://django-downloadview.readthedocs.io
* PyPI page: http://pypi.python.org/pypi/django-downloadview
* Code repository: https://github.com/jazzband/django-downloadview
* Bugtracker: https://github.com/jazzband/django-downloadview/issues
* Continuous integration: https://github.com/jazzband/django-downloadview/actions
* Roadmap: https://github.com/jazzband/django-downloadview/milestones

.. _`Django`: https://djangoproject.com
