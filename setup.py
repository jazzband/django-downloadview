# -*- coding: utf-8 -*-
"""Python packaging."""
import os
import sys

from setuptools import setup


#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2


NAME = 'django-downloadview'
DESCRIPTION = 'Serve files with Django and reverse-proxies.'
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
AUTHOR = u'Benoît Bryon'
EMAIL = 'benoit@marmelune.net'
URL = 'https://{name}.readthedocs.org/'.format(name=NAME)
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'License :: OSI Approved :: BSD License',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.3',
               'Framework :: Django']
KEYWORDS = ['file',
            'stream',
            'download',
            'FileField',
            'ImageField',
            'x-accel',
            'x-accel-redirect',
            'x-sendfile',
            'sendfile',
            'mod_xsendfile',
            'offload']
PACKAGES = [NAME.replace('-', '_')]
REQUIREMENTS = ['setuptools', 'Django>=1.5', 'requests', 'six']
if IS_PYTHON2:
    REQUIREMENTS.append('mock')
ENTRY_POINTS = {}


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=README,
          classifiers=CLASSIFIERS,
          keywords=' '.join(KEYWORDS),
          author=AUTHOR,
          author_email=EMAIL,
          url=URL,
          license='BSD',
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIREMENTS,
          entry_points=ENTRY_POINTS)
