from six import StringIO

from django.core.files.base import ContentFile

from django_downloadview import VirtualDownloadView
from django_downloadview import VirtualFile
from django_downloadview import TextIteratorIO


class TextDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        return ContentFile(b"Hello world!\n", name='hello-world.txt')


class StringIODownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``six.StringIO`` object."""
        file_obj = StringIO(u"Hello world!\n")
        return VirtualFile(file_obj, name='hello-world.txt')


def generate_hello():
    yield u'Hello '
    yield u'world!'
    yield u'\n'


class GeneratedDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``StringIteratorIO`` object."""
        file_obj = TextIteratorIO(generate_hello())
        return VirtualFile(file_obj, name='hello-world.txt')
