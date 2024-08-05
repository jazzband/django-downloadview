############
Demo project
############

`Demo folder in project's repository`_ contains a Django project to illustrate
``django-downloadview`` usage.


*****************************************
Documentation includes code from the demo
*****************************************

Almost every example in the documentation comes from the demo:

* discover examples in the documentation;
* browse related code and tests in demo project.

Examples in documentation are tested via demo project!


***********************
Browse demo code online
***********************

See `demo folder in project's repository`_.


***************
Deploy the demo
***************

System requirements:

* `Python`_ version 3.7+, available as ``python`` command.

  .. note::

     You may use `Virtualenv`_ to make sure the active ``python`` is the right
     one.

* ``make`` and ``wget`` to use the provided :file:`Makefile`.

Execute:

.. code-block:: sh

   git clone git@github.com:jazzband/django-downloadview.git
   cd django-downloadview/
   make runserver

It installs and runs the demo server on localhost, port 8000. So have a look
at ``http://localhost:8000/``.

.. note::

   If you cannot execute the Makefile, read it and adapt the few commands it
   contains to your needs.

Browse and use :file:`demo/demoproject/` as a sandbox.


**********
References
**********

.. target-notes::

.. _`demo folder in project's repository`:
   https://github.com/jazzband/django-downloadview/tree/master/demo/demoproject/

.. _`Python`: http://python.org
.. _`Virtualenv`: http://virtualenv.org
