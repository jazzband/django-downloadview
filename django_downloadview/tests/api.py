# -*- coding: utf-8 -*-
"""Test suite around :mod:`django_downloadview.api` and deprecation plan."""
import unittest
import warnings

from django.core.exceptions import ImproperlyConfigured
import django.test
from django.test.utils import override_settings
from django.utils.importlib import import_module


class APITestCase(unittest.TestCase):
    """Make sure django_downloadview exposes API."""
    def assert_module_attributes(self, module_path, attribute_names):
        """Assert imported ``module_path`` has ``attribute_names``."""
        module = import_module(module_path)
        missing_attributes = []
        for attribute_name in attribute_names:
            if not hasattr(module, attribute_name):
                missing_attributes.append(attribute_name)
        if missing_attributes:
            self.fail('Missing attributes in "{module}": {attributes}'.format(
                module=module_path, attributes=', '.join(missing_attributes)))

    def test_root_attributes(self):
        """API is exposed in django_downloadview root package.

        The goal of this test is to make sure that main items of project's API
        are easy to import... and prevent refactoring from breaking main API.

        If this test is broken by refactoring, a :class:`DeprecationWarning` or
        simimar should be raised.

        """
        api = [
            # Views:
            'ObjectDownloadView',
            'StorageDownloadView',
            'PathDownloadView',
            'HTTPDownloadView',
            'VirtualDownloadView',
            'BaseDownloadView',
            'DownloadMixin',
            # File wrappers:
            'StorageFile',
            'HTTPFile',
            'VirtualFile',
            # Responses:
            'DownloadResponse',
            'ProxiedDownloadResponse',
            # Middlewares:
            'BaseDownloadMiddleware',
            'DownloadDispatcherMiddleware',
            'SmartDownloadMiddleware',
            # Testing:
            'assert_download_response',
            'setup_view',
            'temporary_media_root',
            # Utilities:
            'StringIteratorIO',
            'sendfile']
        self.assert_module_attributes('django_downloadview', api)

    def test_nginx_attributes(self):
        """Nginx-related API is exposed in django_downloadview.nginx."""
        api = [
            'XAccelRedirectResponse',
            'XAccelRedirectMiddleware',
            'x_accel_redirect',
            'assert_x_accel_redirect']
        self.assert_module_attributes('django_downloadview.nginx', api)


class DeprecatedAPITestCase(django.test.SimpleTestCase):
    """Make sure using deprecated items raise DeprecationWarning."""
    def test_nginx_x_accel_redirect_middleware(self):
        "XAccelRedirectMiddleware in settings triggers ImproperlyConfigured."
        with override_settings(
            MIDDLEWARE_CLASSES=[
                'django_downloadview.nginx.XAccelRedirectMiddleware']):
            with self.assertRaises(ImproperlyConfigured):
                import django_downloadview.nginx.settings
                reload(django_downloadview.nginx.settings)

    def test_nginx_x_accel_redirect_global_settings(self):
        """Global settings for Nginx middleware are deprecated."""
        settings_overrides = {
            'NGINX_DOWNLOAD_MIDDLEWARE_WITH_BUFFERING': True,
            'NGINX_DOWNLOAD_MIDDLEWARE_LIMIT_RATE': 32,
            'NGINX_DOWNLOAD_MIDDLEWARE_EXPIRES': 3600,
            'NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_ROOT': '/',
            'NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_DIR': '/',
            'NGINX_DOWNLOAD_MIDDLEWARE_SOURCE_URL': '/',
            'NGINX_DOWNLOAD_MIDDLEWARE_MEDIA_URL': '/',
            'NGINX_DOWNLOAD_MIDDLEWARE_DESTINATION_URL': '/',
        }
        import django_downloadview.nginx.settings
        missed_warnings = []
        for setting_name, setting_value in settings_overrides.items():
            warnings.resetwarnings()
            warnings.simplefilter("always")
            with warnings.catch_warnings(record=True) as warning_list:
                with override_settings(**{setting_name: setting_value}):
                    reload(django_downloadview.nginx.settings)
            caught = False
            for warning_item in warning_list:
                if warning_item.category == DeprecationWarning:
                    if 'deprecated' in str(warning_item.message):
                        if setting_name in str(warning_item.message):
                            caught = True
                            break
            if not caught:
                missed_warnings.append(setting_name)
        if missed_warnings:
            self.fail(
                'No DeprecationWarning raised about following settings: '
                '{settings}.'.format(settings=', '.join(missed_warnings)))
