"""Testing utilities."""
import shutil
import tempfile

from django.conf import settings
from django.test.utils import override_settings


class temporary_media_root(override_settings):
    """Context manager or decorator to override settings.MEDIA_ROOT.

    >>> from django_downloadview.test import temporary_media_root
    >>> from django.conf import settings
    >>> global_media_root = settings.MEDIA_ROOT
    >>> with temporary_media_root():
    ...     global_media_root == settings.MEDIA_ROOT
    False
    >>> global_media_root == settings.MEDIA_ROOT
    True

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
