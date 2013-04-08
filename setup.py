# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read().strip()


NAME = 'django-downloadview'
README = read_relative_file('README')
VERSION = read_relative_file('VERSION')
PACKAGES = ['django_downloadview']
REQUIRES = ['setuptools', 'django>=1.5', 'requests']


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version=VERSION,
          description='Generic download views for Django.',
          long_description=README,
          classifiers=['Development Status :: 4 - Beta',
                       'License :: OSI Approved :: BSD License',
                       'Programming Language :: Python :: 2.7',
                       'Programming Language :: Python :: 2.6',
                       'Framework :: Django',
                       ],
          keywords='class-based view, generic view, download, file, '
                   'FileField, ImageField, nginx, x-accel, x-sendfile',
          author='Benoît Bryon',
          author_email='benoit@marmelune.net',
          url='https://github.com/benoitbryon/%s' % NAME,
          license='BSD',
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIRES,
          )
