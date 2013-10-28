from StringIO import StringIO

from django.core.files.base import ContentFile

from django_downloadview import VirtualDownloadView
from django_downloadview import VirtualFile
from django_downloadview import StringIteratorIO


class TextDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        return ContentFile(u"Hello world!\n", name='hello-world.txt')


class StringIODownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``StringIO`` object."""
        file_obj = StringIO(u"Hello world!\n".encode('utf-8'))
        return VirtualFile(file_obj, name='hello-world.txt')


def generate_hello():
    yield u'Hello '
    yield u'world!'
    yield u'\n'


class GeneratedDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return wrapper on ``StringIteratorIO`` object."""
        file_obj = StringIteratorIO(generate_hello())
        return VirtualFile(file_obj, name='hello-world.txt')
