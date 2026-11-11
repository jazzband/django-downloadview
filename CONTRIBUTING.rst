############
Contributing
############


This is a `Django Commons <https://github.com/django-commons>`_ project. By
contributing you agree to abide by the `Django Commons Code of Conduct
<https://github.com/django-commons/membership/blob/main/CODE_OF_CONDUCT.md>`_.


This document provides guidelines for people who want to contribute to
``django-downloadview``.


**************
Create tickets
**************

Please use the `bugtracker`_ **before** starting some work:

* check if the bug or feature request has already been filed. It may have been
  answered too!

* else create a new ticket.

* if you plan to contribute, tell us, so that we are given an opportunity to
  give feedback as soon as possible.

* Then, in your commit messages, reference the ticket with some
  ``refs #TICKET-ID`` syntax.


******************
Use topic branches
******************

* Work in branches.

* Prefix your branch with the ticket ID corresponding to the issue. As an
  example, if you are working on ticket #23 which is about contribute
  documentation, name your branch like ``23-contribute-doc``.

* If you work in a development branch and want to refresh it with changes from
  master, please `rebase`_ or `merge-based rebase`_, i.e. do not merge master.


***********
Fork, clone
***********

Clone ``django-downloadview`` repository (adapt to use your own fork):

.. code:: sh

   git clone git@github.com:django-commons/django-downloadview.git
   cd django-downloadview/


*************
Running tests
*************

Tests are run with `tox`_ against every supported combination of Python and
Django:

.. code:: sh

   pip install tox
   tox

To run a single environment, for instance Python 3.12 with Django 5.2 and
pytest:

.. code:: sh

   tox -e py312-dj52-pytest

List the available environments with ``tox -l``.

Code style is checked with `pre-commit`_. Install the hooks once, so that they
run on every commit, or run them manually on the whole repository:

.. code:: sh

   pip install pre-commit
   pre-commit install
   pre-commit run --all-files


*************
Usual actions
*************

The ``Makefile`` is the reference card for usual actions in development
environment:

* Install development toolkit with `pip`_: ``make develop``.

* Run tests with `tox`_: ``make test``.

* Build documentation: ``make documentation``. It builds `Sphinx`_
  documentation in ``var/docs/html/index.html``.

* Cleanup local repository: ``make clean``, ``make distclean`` and
  ``make maintainer-clean``.

See also ``make help``.


*********************
Demo project included
*********************

The ``demo`` included in project's repository is part of the tests and
documentation. Maintain it along with code and documentation.


*********
Releasing
*********

Releases are published to `PyPI`_ by GitHub Actions, using PyPI's
`Trusted Publishing`_. To make a release, update the ``CHANGELOG``, then push
a tag named after the version. The version is computed from the tag.


.. rubric:: Notes & references

.. target-notes::

.. _`bugtracker`:
   https://github.com/django-commons/django-downloadview/issues
.. _`rebase`: http://git-scm.com/book/en/Git-Branching-Rebasing
.. _`merge-based rebase`: https://tech.people-doc.com/psycho-rebasing.html
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`tox`: https://tox.readthedocs.io/
.. _`Sphinx`: https://pypi.python.org/pypi/Sphinx/
.. _`pre-commit`: https://pre-commit.com/
.. _`PyPI`: https://pypi.org/project/django-downloadview/
.. _`Trusted Publishing`: https://docs.pypi.org/trusted-publishers/
