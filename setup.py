import os

from setuptools import setup

#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="django-downloadview",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description="Serve files with Django and reverse-proxies.",
    long_description=open(os.path.join(here, "README.rst")).read(),  # noqa: SIM115
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Framework :: Django :: 6.1",
    ],
    keywords="file stream download FileField ImageField x-accel x-accel-redirect x-sendfile sendfile mod_xsendfile offload",
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
    python_requires=">=3.11",
    install_requires=[
        # BEGIN requirements
        "Django>=4.2",
        "requests",
        # END requirements
    ],
    extras_require={
        "test": ["tox"],
    },
)
