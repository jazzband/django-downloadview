"""Django settings for django-downloadview demo project."""
import os


# Configure some relative directories.
demoproject_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(demoproject_dir)
root_dir = os.path.dirname(demo_dir)
data_dir = os.path.join(root_dir, "var")
cfg_dir = os.path.join(root_dir, "etc")


# Mandatory settings.
ROOT_URLCONF = "demoproject.urls"
WSGI_APPLICATION = "demoproject.wsgi.application"


# Database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(data_dir, "db.sqlite"),
    }
}


# Required.
SECRET_KEY = "This is a secret made public on project's repository."

# Media and static files.
MEDIA_ROOT = os.path.join(data_dir, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(data_dir, "static")
STATIC_URL = "/static/"


# Applications.
INSTALLED_APPS = (
    # The actual django-downloadview demo.
    "demoproject",
    "demoproject.object",  # Demo around ObjectDownloadView
    "demoproject.storage",  # Demo around StorageDownloadView
    "demoproject.path",  # Demo around PathDownloadView
    "demoproject.http",  # Demo around HTTPDownloadView
    "demoproject.virtual",  # Demo around VirtualDownloadView
    "demoproject.nginx",  # Sample optimizations for Nginx X-Accel.
    "demoproject.apache",  # Sample optimizations for Apache X-Sendfile.
    "demoproject.lighttpd",  # Sample optimizations for Lighttpd X-Sendfile.
    # Standard Django applications.
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)


# BEGIN middlewares
MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_downloadview.SmartDownloadMiddleware",
]
# END middlewares


# Specific configuration for django_downloadview.SmartDownloadMiddleware.
# BEGIN backend
DOWNLOADVIEW_BACKEND = "django_downloadview.nginx.XAccelRedirectMiddleware"
# END backend
"""Could also be:
DOWNLOADVIEW_BACKEND = 'django_downloadview.apache.XSendfileMiddleware'
DOWNLOADVIEW_BACKEND = 'django_downloadview.lighttpd.XSendfileMiddleware'
"""

# BEGIN rules
DOWNLOADVIEW_RULES = [
    {
        "source_url": "/media/nginx/",
        "destination_url": "/nginx-optimized-by-middleware/",
    },
]
# END rules
DOWNLOADVIEW_RULES += [
    {
        "source_url": "/media/apache/",
        "destination_dir": "/apache-optimized-by-middleware/",
        # Bypass global default backend with additional argument "backend".
        # Notice that in general use case, ``DOWNLOADVIEW_BACKEND`` should be
        # enough. Here, the django_downloadview demo project needs to
        # demonstrate usage of several backends.
        "backend": "django_downloadview.apache.XSendfileMiddleware",
    },
    {
        "source_url": "/media/lighttpd/",
        "destination_dir": "/lighttpd-optimized-by-middleware/",
        # Bypass global default backend with additional argument "backend".
        # Notice that in general use case, ``DOWNLOADVIEW_BACKEND`` should be
        # enough. Here, the django_downloadview demo project needs to
        # demonstrate usage of several backends.
        "backend": "django_downloadview.lighttpd.XSendfileMiddleware",
    },
]


# Test/development settings.
DEBUG = True


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
