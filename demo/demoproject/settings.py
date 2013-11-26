# -*- coding: utf-8 -*-
"""Django settings for Django-DownloadView demo project."""
from os.path import abspath, dirname, join


# Configure some relative directories.
demoproject_dir = dirname(abspath(__file__))
demo_dir = dirname(demoproject_dir)
root_dir = dirname(demo_dir)
data_dir = join(root_dir, 'var')
cfg_dir = join(root_dir, 'etc')


# Mandatory settings.
ROOT_URLCONF = 'demoproject.urls'
WSGI_APPLICATION = 'demoproject.wsgi.application'


# Database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(data_dir, 'db.sqlite'),
    }
}


# Required.
SECRET_KEY = "This is a secret made public on project's repository."

# Media and static files.
MEDIA_ROOT = join(data_dir, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = join(data_dir, 'static')
STATIC_URL = '/static/'


# Applications.
INSTALLED_APPS = (
    # Standard Django applications.
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The actual django-downloadview demo.
    'demoproject',
    'demoproject.object',  # Demo around ObjectDownloadView
    'demoproject.storage',  # Demo around StorageDownloadView
    'demoproject.path',  # Demo around PathDownloadView
    'demoproject.http',  # Demo around HTTPDownloadView
    'demoproject.virtual',  # Demo around VirtualDownloadView
    'demoproject.nginx',  # Sample optimizations for Nginx X-Accel.
    'demoproject.apache',  # Sample optimizations for Apache X-Sendfile.
    # For test purposes. The demo project is part of django-downloadview
    # test suite.
    'django_nose',
)


# Middlewares.
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_downloadview.SmartDownloadMiddleware'
]


# Specific configuration for django_downloadview.SmartDownloadMiddleware.
DOWNLOADVIEW_BACKEND = 'django_downloadview.nginx.XAccelRedirectMiddleware'
"""Could also be:
DOWNLOADVIEW_BACKEND = 'django_downloadview.apache.XSendfileMiddleware'
"""
DOWNLOADVIEW_RULES = [
    {
        'source_url': '/media/nginx/',
        'destination_url': '/nginx-optimized-by-middleware/',
    },
    {
        'source_url': '/media/apache/',
        'destination_dir': '/apache-optimized-by-middleware/',
        # Bypass global default backend with additional argument "backend".
        # Notice that in general use case, ``DOWNLOADVIEW_BACKEND`` should be
        # enough. Here, the django_downloadview demo project needs to
        # demonstrate usage of several backends.
        'backend': 'django_downloadview.apache.XSendfileMiddleware',
    },
]


# Test/development settings.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
nose_cfg_dir = join(cfg_dir, 'nose')
NOSE_ARGS = ['--config={etc}/base.cfg'.format(etc=nose_cfg_dir),
             '--config={etc}/{package}.cfg'.format(etc=nose_cfg_dir,
                                                   package=__package__)]
