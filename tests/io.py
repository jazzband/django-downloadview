"""Tests around :mod:`django_downloadview.io`."""
import unittest

from django_downloadview import BytesIteratorIO, TextIteratorIO

HELLO_TEXT = "Hello world!\né\n"
HELLO_BYTES = b"Hello world!\n\xc3\xa9\n"


def generate_hello_text():
    """Generate u'Hello world!\n'."""
    yield "Hello "
    yield "world!"
    yield "\n"
    yield "é"
    yield "\n"


def generate_hello_bytes():
    """Generate b'Hello world!\n'."""
    yield b"Hello "
    yield b"world!"
    yield b"\n"
    yield b"\xc3\xa9"
    yield b"\n"


class TextIteratorIOTestCase(unittest.TestCase):
    """Tests around :class:`~django_downloadview.io.TextIteratorIO`."""

    def test_read_text(self):
        """TextIteratorIO obviously accepts text generator."""
        file_obj = TextIteratorIO(generate_hello_text())
        self.assertEqual(file_obj.read(), HELLO_TEXT)

    def test_read_bytes(self):
        """TextIteratorIO converts bytes as text."""
        file_obj = TextIteratorIO(generate_hello_bytes())
        self.assertEqual(file_obj.read(), HELLO_TEXT)


class BytesIteratorIOTestCase(unittest.TestCase):
    """Tests around :class:`~django_downloadview.io.BytesIteratorIO`."""

    def test_read_bytes(self):
        """BytesIteratorIO obviously accepts bytes generator."""
        file_obj = BytesIteratorIO(generate_hello_bytes())
        self.assertEqual(file_obj.read(), HELLO_BYTES)

    def test_read_text(self):
        """BytesIteratorIO converts text as bytes."""
        file_obj = BytesIteratorIO(generate_hello_text())
        self.assertEqual(file_obj.read(), HELLO_BYTES)
