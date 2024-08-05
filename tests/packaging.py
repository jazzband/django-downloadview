"""Tests around project's distribution and packaging."""

import importlib.metadata
import os
import unittest

tests_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(tests_dir)
build_dir = os.path.join(project_dir, "var", "docs", "html")


class VersionTestCase(unittest.TestCase):
    """Various checks around project's version info."""

    def get_version(self):
        """Return django_downloadview.__version__."""
        from django_downloadview import __version__

        return __version__

    def test_version_present(self):
        """:PEP:`396` - django_downloadview has __version__ attribute."""
        try:
            self.get_version()
        except ImportError:
            self.fail("django_downloadview package has no __version__.")

    def test_version_match(self):
        """django_downloadview.__version__ matches importlib metadata."""
        distribution = importlib.metadata.distribution("django-downloadview")
        installed_version = distribution.version
        self.assertEqual(
            installed_version,
            self.get_version(),
            "Version mismatch: django_downloadview.__version__ "
            'is "%s" whereas importlib.metadata tells "%s". '
            "You may need to run ``make develop`` to update the "
            "installed version in development environment."
            % (self.get_version(), installed_version),
        )
