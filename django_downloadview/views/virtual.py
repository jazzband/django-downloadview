# -*- coding: utf-8 -*-
"""Stream files that you generate or that live in memory."""
from django_downloadview.views.base import BaseDownloadView


class VirtualDownloadView(BaseDownloadView):
    """Serve not-on-disk or generated-on-the-fly file.

    Override the :py:meth:`get_file` method to customize file wrapper.

    """
    def was_modified_since(self, file_instance, since):
        """Delegate to file wrapper's was_modified_since, or return True.

        This is the implementation of an edge case: when files are generated
        on the fly, we cannot guess whether they have been modified or not.
        If the file wrapper implements ``was_modified_since()`` method, then we
        trust it. Otherwise it is safer to suppose that the file has been
        modified.

        This behaviour prevents file size to be computed on the Django side.
        Because computing file size means iterating over all the file contents,
        and we want to avoid that whenever possible. As an example, it could
        reduce all the benefits of working with dynamic file generators...
        which is a major feature of virtual files.

        """
        try:
            return file_instance.was_modified_since(since)
        except (AttributeError, NotImplementedError):
            return True
