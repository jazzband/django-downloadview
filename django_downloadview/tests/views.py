# -*- coding: utf-8 -*-
"""Unit tests around views."""
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from django.http import Http404
from django.http.response import HttpResponseNotModified
import django.test

from django_downloadview import exceptions
from django_downloadview.test import setup_view
from django_downloadview import views


class DownloadMixinTestCase(unittest.TestCase):
    """Tests around :class:`django_downloadviews.views.base.DownloadMixin`."""
    def test_get_file(self):
        """DownloadMixin.get_file() raise NotImplementedError.

        Subclasses must implement it!

        """
        mixin = views.DownloadMixin()
        with self.assertRaises(NotImplementedError):
            mixin.get_file()

    def test_get_basename(self):
        """DownloadMixin.get_basename() returns basename attribute."""
        mixin = views.DownloadMixin()
        self.assertEqual(mixin.get_basename(), None)
        mixin.basename = 'fake'
        self.assertEqual(mixin.get_basename(), 'fake')

    def test_was_modified_since_file(self):
        """DownloadMixin.was_modified_since() tries (1) file's implementation.

        :meth:`django_downloadview.views.base.DownloadMixin.was_modified_since`
        first tries to delegate computations to file wrapper's implementation.

        """
        file_wrapper = mock.Mock()
        file_wrapper.was_modified_since = mock.Mock(
            return_value=mock.sentinel.was_modified)
        mixin = views.DownloadMixin()
        self.assertIs(
            mixin.was_modified_since(file_wrapper, mock.sentinel.since),
            mock.sentinel.was_modified)
        file_wrapper.was_modified_since.assertCalledOnceWith(
            mock.sentinel.since)

    def test_was_modified_since_django(self):
        """DownloadMixin.was_modified_since() tries (2) files attributes.

        When calling file wrapper's ``was_modified_since()`` raises
        ``NotImplementedError`` or ``AttributeError``,
        :meth:`django_downloadview.views.base.DownloadMixin.was_modified_since`
        tries to pass file wrapper's ``size`` and ``modified_time`` to
        :func:`django.views.static import was_modified_since`.

        """
        file_wrapper = mock.Mock()
        file_wrapper.was_modified_since = mock.Mock(
            side_effect=AttributeError)
        file_wrapper.size = mock.sentinel.size
        file_wrapper.modified_time = mock.sentinel.modified_time
        was_modified_since_mock = mock.Mock(
            return_value=mock.sentinel.was_modified)
        mixin = views.DownloadMixin()
        with mock.patch('django_downloadview.views.base.was_modified_since',
                        new=was_modified_since_mock):
            self.assertIs(
                mixin.was_modified_since(file_wrapper, mock.sentinel.since),
                mock.sentinel.was_modified)
        was_modified_since_mock.assertCalledOnceWith(
            mock.sentinel.size,
            mock.sentinel.modified_time)

    def test_was_modified_since_fallback(self):
        """DownloadMixin.was_modified_since() fallbacks to `True`.

        When:

        * calling file wrapper's ``was_modified_since()`` raises
          ``NotImplementedError`` or ``AttributeError``;

        * and accessing ``size`` and ``modified_time`` from file wrapper raises
          ``NotImplementedError`` or ``AttributeError``...

        ... then
        :meth:`django_downloadview.views.base.DownloadMixin.was_modified_since`
        returns ``True``.

        """
        file_wrapper = mock.Mock()
        file_wrapper.was_modified_since = mock.Mock(
            side_effect=NotImplementedError)
        type(file_wrapper).modified_time = mock.PropertyMock(
            side_effect=NotImplementedError)
        mixin = views.DownloadMixin()
        self.assertIs(
            mixin.was_modified_since(file_wrapper, 'fake since'),
            True)

    def test_not_modified_response(self):
        "DownloadMixin.not_modified_response returns HttpResponseNotModified."
        mixin = views.DownloadMixin()
        response = mixin.not_modified_response()
        self.assertTrue(isinstance(response, HttpResponseNotModified))

    def test_download_response(self):
        "DownloadMixin.download_response() returns download response instance."
        mixin = views.DownloadMixin()
        mixin.file_instance = mock.sentinel.file_wrapper
        response_factory = mock.Mock(return_value=mock.sentinel.response)
        mixin.response_class = response_factory
        response_kwargs = {'dummy': 'value',
                           'file_instance': mock.sentinel.file_wrapper,
                           'attachment': True,
                           'basename': None}
        response = mixin.download_response(**response_kwargs)
        self.assertIs(response, mock.sentinel.response)
        response_factory.assert_called_once_with(**response_kwargs)  # Not args

    def test_render_to_response_not_modified(self):
        """DownloadMixin.render_to_response() respects HTTP_IF_MODIFIED_SINCE
        header (calls ``not_modified_response()``)."""
        # Setup.
        mixin = views.DownloadMixin()
        mixin.request = django.test.RequestFactory().get(
            '/dummy-url',
            HTTP_IF_MODIFIED_SINCE=mock.sentinel.http_if_modified_since)
        mixin.was_modified_since = mock.Mock(return_value=False)
        mixin.not_modified_response = mock.Mock(
            return_value=mock.sentinel.http_not_modified_response)
        mixin.get_file = mock.Mock(return_value=mock.sentinel.file_wrapper)
        # Run.
        response = mixin.render_to_response()
        # Check.
        self.assertIs(response, mock.sentinel.http_not_modified_response)
        mixin.get_file.assert_called_once_with()
        mixin.was_modified_since.assert_called_once_with(
            mock.sentinel.file_wrapper,
            mock.sentinel.http_if_modified_since)
        mixin.not_modified_response.assert_called_once_with()

    def test_render_to_response_modified(self):
        """DownloadMixin.render_to_response() calls download_response()."""
        # Setup.
        mixin = views.DownloadMixin()
        mixin.request = django.test.RequestFactory().get(
            '/dummy-url',
            HTTP_IF_MODIFIED_SINCE=None)
        mixin.was_modified_since = mock.Mock()
        mixin.download_response = mock.Mock(
            return_value=mock.sentinel.download_response)
        mixin.get_file = mock.Mock(return_value=mock.sentinel.file_wrapper)
        # Run.
        response = mixin.render_to_response()
        # Check.
        self.assertIs(response, mock.sentinel.download_response)
        mixin.get_file.assert_called_once_with()
        self.assertEqual(mixin.was_modified_since.call_count, 0)
        mixin.download_response.assert_called_once_with()

    def test_render_to_response_file_not_found(self):
        "DownloadMixin.render_to_response() calls file_not_found_response()."
        # Setup.
        mixin = views.DownloadMixin()
        mixin.request = django.test.RequestFactory().get('/dummy-url')
        mixin.get_file = mock.Mock(side_effect=exceptions.FileNotFound)
        mixin.file_not_found_response = mock.Mock()
        # Run.
        mixin.render_to_response()
        # Check.
        mixin.file_not_found_response.assert_called_once_with()

    def test_file_not_found_response(self):
        """DownloadMixin.file_not_found_response() raises Http404."""
        mixin = views.DownloadMixin()
        with self.assertRaises(Http404):
            mixin.file_not_found_response()


class BaseDownloadViewTestCase(unittest.TestCase):
    "Tests around :class:`django_downloadviews.views.base.BaseDownloadView`."
    def test_get(self):
        """BaseDownloadView.get() calls render_to_response()."""
        request = django.test.RequestFactory().get('/dummy-url')
        args = ['dummy-arg']
        kwargs = {'dummy': 'kwarg'}
        view = setup_view(views.BaseDownloadView(), request, *args, **kwargs)
        view.render_to_response = mock.Mock(
            return_value=mock.sentinel.response)
        response = view.get(request, *args, **kwargs)
        self.assertIs(response, mock.sentinel.response)
        view.render_to_response.assert_called_once_with()


class ObjectDownloadViewTestCase(unittest.TestCase):
    "Tests for :class:`django_downloadviews.views.object.ObjectDownloadView`."
    def test_get_file_ok(self):
        "ObjectDownloadView.get_file() returns ``file`` field by default."
        view = setup_view(views.ObjectDownloadView(), 'fake request')
        view.object = mock.Mock(spec=['file'])
        view.get_file()

    def test_get_file_wrong_field(self):
        """ObjectDownloadView.get_file() raises AttributeError if field does
        not exist.

        ``AttributeError`` is expected because this is a configuration error,
        i.e. it is related to Python code.

        """
        view = setup_view(views.ObjectDownloadView(file_field='other_field'),
                          'fake request')
        view.object = mock.Mock(spec=['file'])
        with self.assertRaises(AttributeError):
            view.get_file()

    def test_get_file_empty_field(self):
        """ObjectDownloadView.get_file() raises FileNotFound if field does not
        exist."""
        view = setup_view(views.ObjectDownloadView(file_field='other_field'),
                          'fake request')
        view.object = mock.Mock()
        view.object.other_field = None
        with self.assertRaises(exceptions.FileNotFound):
            view.get_file()
