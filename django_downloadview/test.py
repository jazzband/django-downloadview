"""Testing utilities."""
import shutil
from six import iteritems
import tempfile

from django.conf import settings
from django.test.utils import override_settings

from django_downloadview.middlewares import is_download_response
from django_downloadview.response import (encode_basename_ascii,
                                          encode_basename_utf8)


def setup_view(view, request, *args, **kwargs):
    """Mimic ``as_view()``, but returns view instance.

    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.

    This is an early implementation of
    https://code.djangoproject.com/ticket/20456

    ``view``
        A view instance, such as ``TemplateView(template_name='dummy.html')``.
        Initialization arguments are the same you would pass to ``as_view()``.

    ``request``
        A request object, typically built with
        :class:`~django.test.client.RequestFactory`.

    ``args`` and ``kwargs``
        "URLconf" positional and keyword arguments, the same you would pass to
        :func:`~django.core.urlresolvers.reverse`.

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class temporary_media_root(override_settings):
    """Temporarily override settings.MEDIA_ROOT with a temporary directory.

    The temporary directory is automatically created and destroyed.

    Use this function as a context manager:

    >>> from django_downloadview.test import temporary_media_root
    >>> from django.conf import settings  # NoQA
    >>> global_media_root = settings.MEDIA_ROOT
    >>> with temporary_media_root():
    ...     global_media_root == settings.MEDIA_ROOT
    False
    >>> global_media_root == settings.MEDIA_ROOT
    True

    Or as a decorator:

    >>> @temporary_media_root()
    ... def use_temporary_media_root():
    ...     return settings.MEDIA_ROOT
    >>> tmp_media_root = use_temporary_media_root()
    >>> global_media_root == tmp_media_root
    False
    >>> global_media_root == settings.MEDIA_ROOT
    True

    """
    def enable(self):
        """Create a temporary directory and use it to override
        settings.MEDIA_ROOT."""
        tmp_dir = tempfile.mkdtemp()
        self.options['MEDIA_ROOT'] = tmp_dir
        super(temporary_media_root, self).enable()

    def disable(self):
        """Remove directory settings.MEDIA_ROOT then restore original
        setting."""
        shutil.rmtree(settings.MEDIA_ROOT)
        super(temporary_media_root, self).disable()


class DownloadResponseValidator(object):
    """Utility class to validate DownloadResponse instances."""
    def __call__(self, test_case, response, **assertions):
        """Assert that ``response`` is a valid DownloadResponse instance.

        Optional ``assertions`` dictionary can be used to check additional
        items:

        * ``basename``: the basename of the file in the response.

        * ``content_type``: the value of "Content-Type" header.

        * ``mime_type``: the MIME type part of "Content-Type" header (without
          charset).

        * ``content``: the contents of the file.

        * ``attachment``: whether the file is returned as attachment or not.

        """
        self.assert_download_response(test_case, response)
        for key, value in iteritems(assertions):
            assert_func = getattr(self, 'assert_%s' % key)
            assert_func(test_case, response, value)

    def assert_download_response(self, test_case, response):
        test_case.assertTrue(is_download_response(response))

    def assert_basename(self, test_case, response, value):
        """Implies ``attachement is True``."""
        ascii_name = encode_basename_ascii(value)
        utf8_name = encode_basename_utf8(value)
        check_utf8 = False
        check_ascii = False
        if ascii_name == utf8_name:  # Only ASCII characters.
            check_ascii = True
            if "filename*=" in response['Content-Disposition']:
                check_utf8 = True
        else:
            check_utf8 = True
            if "filename=" in response['Content-Disposition']:
                check_ascii = True
        if check_ascii:
            test_case.assertIn('filename="{name}"'.format(
                name=ascii_name),
                response['Content-Disposition'])
        if check_utf8:
            test_case.assertIn(
                "filename*=UTF-8''{name}".format(name=utf8_name),
                response['Content-Disposition'])

    def assert_content_type(self, test_case, response, value):
        test_case.assertEqual(response['Content-Type'], value)

    def assert_mime_type(self, test_case, response, value):
        test_case.assertTrue(response['Content-Type'].startswith(value))

    def assert_content(self, test_case, response, value):
        test_case.assertEqual(
            ''.join([s.decode('utf-8') for s in response.streaming_content]),
            value)

    def assert_attachment(self, test_case, response, value):
        if value:
            test_case.assertTrue(
                'attachment;' in response['Content-Disposition'])
        else:
            test_case.assertTrue(
                'Content-Disposition' not in response
                or 'attachment;' not in response['Content-Disposition'])


def assert_download_response(test_case, response, **assertions):
    """Make ``test_case`` assert that ``response`` meets ``assertions``.

    Optional ``assertions`` dictionary can be used to check additional items:

    * ``basename``: the basename of the file in the response.

    * ``content_type``: the value of "Content-Type" header.

    * ``mime_type``: the MIME type part of "Content-Type" header (without
      charset).

    * ``content``: the contents of the file.

    * ``attachment``: whether the file is returned as attachment or not.

    """
    validator = DownloadResponseValidator()
    return validator(test_case, response, **assertions)
