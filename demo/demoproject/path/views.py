import os

from django_downloadview import PathDownloadView

# Let's initialize some fixtures.
app_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(app_dir)
fixtures_dir = os.path.join(project_dir, "fixtures")
#: Path to a text file that says 'Hello world!'.
hello_world_path = os.path.join(fixtures_dir, "hello-world.txt")

#: Serve ``fixtures/hello-world.txt`` file.
static_path = PathDownloadView.as_view(path=hello_world_path)


class DynamicPathDownloadView(PathDownloadView):
    """Serve file in ``settings.MEDIA_ROOT``.

    .. warning::

       Make sure to prevent "../" in path via URL patterns.

    .. note::

       This particular setup would be easier to perform with
       :class:`StorageDownloadView`

    """

    def get_path(self):
        """Return path inside fixtures directory."""
        # Get path from URL resolvers or as_view kwarg.
        relative_path = super(DynamicPathDownloadView, self).get_path()
        # Make it absolute.
        absolute_path = os.path.join(fixtures_dir, relative_path)
        return absolute_path


dynamic_path = DynamicPathDownloadView.as_view()
