# coding=utf-8
"""Tests around :py:mod:`django_downloadview.views`."""
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from django_downloadview import views


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    ``*args`` and ``**kwargs`` are the same you would pass to ``reverse()``

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class DownloadMixinTestCase(unittest.TestCase):
    """Test suite around :py:class:`django_downloadview.views.DownloadMixin`.
    """
    def test_was_modified_since_specific(self):
        """DownloadMixin.was_modified_since() delegates to file wrapper."""
        file_wrapper = mock.Mock()
        file_wrapper.was_modified_since = mock.Mock(
            return_value=mock.sentinel.return_value)
        mixin = views.DownloadMixin()
        since = mock.sentinel.since
        return_value = mixin.was_modified_since(file_wrapper, since)
        self.assertEqual(return_value, mock.sentinel.return_value)
        file_wrapper.was_modified_since.assert_called_once_with(since)

    def test_was_modified_since_not_implemented(self):
        """DownloadMixin.was_modified_since() returns True if file wrapper
        does not support ``modified_time`` or ``size`` attributes."""
        fields = ['modified_time', 'size']
        side_effects = [AttributeError('fake'), NotImplementedError('fake')]
        for field in fields:
            for side_effect in side_effects:
                file_wrapper = mock.Mock()
                setattr(file_wrapper, field, mock.Mock(
                    side_effect=AttributeError('fake')))
                mixin = views.DownloadMixin()
                since = mock.sentinel.since
                self.assertTrue(mixin.was_modified_since(file_wrapper, since))
