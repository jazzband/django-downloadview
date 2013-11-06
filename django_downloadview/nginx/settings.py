# -*- coding: utf-8 -*-
"""Django settings around Nginx X-Accel.

.. warning::

   These settings are deprecated since version 1.3. You can now provide custom
   configuration via `DOWNLOADVIEW_BACKEND` setting. See :doc:`/settings`
   for details.

"""
import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# In version 1.3, former XAccelRedirectMiddleware has been renamed to
# SingleXAccelRedirectMiddleware. So tell the users.
middleware = 'django_downloadview.nginx.XAccelRedirectMiddleware'
if middleware in settings.MIDDLEWARE_CLASSES:
    raise ImproperlyConfigured(
        '{middleware} middleware has been renamed as of django-downloadview '
        'version 1.3. You may use '
        '"django_downloadview.nginx.SingleXAccelRedirectMiddleware" instead, '
        'or upgrade to "django_downloadview.SmartDownloadDispatcher". ')


deprecated_msg = 'settings.{deprecated} is deprecated. You should combine ' \
                 '"django_downloadview.SmartDownloadDispatcher" with ' \
                 'with DOWNLOADVIEW_BACKEND and DOWNLOADVIEW_RULES instead.'


#: Default value for X-Accel-Buffering header.
#: Also default value for
#: ``settings.NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Buffering
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#:
#: If set to ``False``, Nginx buffering is disabled.
#: If set to ``True``, Nginx buffering is enabled.
DEFAULT_WITH_BUFFERING = None
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_WITH_BUFFERING)


#: Default value for X-Accel-Limit-Rate header.
#: Also default value for ``settings.NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Rate
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#:
#: If set to ``False``, Nginx limit rate is disabled.
#: Else, it indicates the limit rate in bytes.
DEFAULT_LIMIT_RATE = None
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_LIMIT_RATE)


#: Default value for X-Accel-Limit-Expires header.
#: Also default value for ``settings.NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES``.
#:
#: See http://wiki.nginx.org/X-accel#X-Accel-Limit-Expires
#:
#: Default value is None, which means "let Nginx choose", i.e. use Nginx
#: defaults or specific configuration.
#:
#: If set to ``False``, Nginx buffering is disabled.
#: Else, it indicates the expiration delay, in seconds.
DEFAULT_EXPIRES = None
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_EXPIRES)


#: Default value for settings.NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR.
DEFAULT_SOURCE_DIR = settings.MEDIA_ROOT
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
    DEFAULT_SOURCE_DIR = settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_SOURCE_DIR)


#: Default value for settings.NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_URL.
DEFAULT_SOURCE_URL = settings.MEDIA_URL
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_URL'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_SOURCE_URL)


#: Default value for settings.NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL.
DEFAULT_DESTINATION_URL = None
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
    DEFAULT_SOURCE_DIR = settings.NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL
setting_name = 'NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL'
if hasattr(settings, setting_name):
    warnings.warn(deprecated_msg.format(deprecated=setting_name),
                  DeprecationWarning)
if not hasattr(settings, setting_name):
    setattr(settings, setting_name, DEFAULT_DESTINATION_URL)
