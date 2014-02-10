############
Contributing
############

This document provides guidelines for people who want to contribute to
`django-downloadview`.


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


***************
Fork and branch
***************

* Work in forks and branches.

* Prefix your branch with the ticket ID corresponding to the issue. As an
  example, if you are working on ticket #23 which is about contribute
  documentation, name your branch like ``23-contribute-doc``.

* If you work in a development branch and want to refresh it with changes from
  master, please `rebase`_ or `merge-based rebase`_, i.e. don't merge master.


*******************************
Setup a development environment
*******************************

System requirements: `Python`_ version 2.7 and `tox`_ (you may use a
`Virtualenv`_).

Execute:

.. code-block:: sh

   git clone git@github.com:benoitbryon/django-downloadview.git
   cd django-downloadview/
   make develop

If you cannot execute the Makefile, read it and adapt the few commands it
contains to your needs.


************
The Makefile
************

A :file:`Makefile` is provided to ease development. Use it to:

* setup a minimal development environment: ``make develop``
* run tests: ``make test``
* build documentation: ``make documentation``

The :file:`Makefile` is intended to be a live reference for the development
environment.


*********************
Demo project included
*********************

The :doc:`/demo` is part of the tests. Maintain it along with code and
documentation.


.. rubric:: Notes & references

.. target-notes::

.. _`bugtracker`: 
   https://github.com/benoitbryon/django-downloadview/issues
.. _`rebase`: http://git-scm.com/book/en/Git-Branching-Rebasing
.. _`merge-based rebase`: http://tech.novapost.fr/psycho-rebasing-en.html
.. _`Python`: http://python.org
.. _`tox`: http://tox.testrun.org
.. _`Virtualenv`: http://virtualenv.org
.. _`style guide for Sphinx-based documentations`:
   http://documentation-style-guide-sphinx.readthedocs.org/
