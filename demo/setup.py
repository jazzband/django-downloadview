# -*- coding: utf-8 -*-
"""Python packaging."""
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(here)


NAME = 'django-downloadview-demo'
DESCRIPTION = 'Serve files with Django and reverse-proxies.'
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(project_root, 'VERSION')).read().strip()
AUTHOR = u'Benoît Bryon'
EMAIL = u'benoit@marmelune.net'
URL = 'https://django-downloadview.readthedocs.io/'
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'License :: OSI Approved :: BSD License',
               'Programming Language :: Python :: 2.7',
               'Framework :: Django']
KEYWORDS = []
PACKAGES = ['demoproject']
REQUIREMENTS = [
    'django-downloadview',
    'django-nose==1.4.3']
ENTRY_POINTS = {
    'console_scripts': ['demo = demoproject.manage:main']
}


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
