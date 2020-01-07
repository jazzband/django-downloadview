from io import StringIO

from django.core.files.base import ContentFile

from django_downloadview import TextIteratorIO, VirtualDownloadView, VirtualFile


class TextDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        return ContentFile(b"Hello world!\n", name="hello-world.txt")


class StringIODownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``six.StringIO`` object."""
        file_obj = StringIO("Hello world!\n")
        return VirtualFile(file_obj, name="hello-world.txt")


def generate_hello():
    yield "Hello "
    yield "world!"
    yield "\n"


class GeneratedDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``StringIteratorIO`` object."""
        file_obj = TextIteratorIO(generate_hello())
        return VirtualFile(file_obj, name="hello-world.txt")
