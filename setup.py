# -*- coding: utf-8 -*-
import os
from setuptools import setup

#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="django-downloadview",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description="Serve files with Django and reverse-proxies.",
    long_description=open(os.path.join(here, "README.rst")).read(),
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=" ".join(
        [
            "file",
            "stream",
            "download",
            "FileField",
            "ImageField",
            "x-accel",
            "x-accel-redirect",
            "x-sendfile",
            "sendfile",
            "mod_xsendfile",
            "offload",
        ]
    ),
    author="Benoît Bryon",
    author_email="benoit@marmelune.net",
    url="https://django-downloadview.readthedocs.io/",
    license="BSD",
    packages=[
        "django_downloadview",
        "django_downloadview.apache",
        "django_downloadview.lighttpd",
        "django_downloadview.nginx",
        "django_downloadview.views",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # BEGIN requirements
        "Django>=1.11",
        "requests",
        "setuptools",
        # END requirements
    ],
    extras_require={
        "test": ["tox"],
    },
)
