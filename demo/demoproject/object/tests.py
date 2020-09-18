from django.core.files.base import ContentFile
import django.test
from django.urls import reverse

from django_downloadview import assert_download_response, temporary_media_root

from demoproject.object.models import Document

# Fixtures.
slug = "hello-world"
basename = "hello-world.txt"
file_name = "file.txt"
another_name = "another_file.txt"
file_content = "Hello world!\n"
another_content = "Goodbye world!\n"


def setup_document():
    document = Document(slug=slug, basename=basename)
    document.file.save(file_name, ContentFile(file_content), save=False)
    document.another_file.save(another_name, ContentFile(another_content), save=False)
    document.save()
    return document


class DefaultFileTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        """'default_file' streams Document.file."""
        setup_document()
        url = reverse("object:default_file", kwargs={"slug": slug})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=file_content,
            basename=file_name,
            mime_type="text/plain",
        )


class AnotherFileTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        """'another_file' streams Document.another_file."""
        setup_document()
        url = reverse("object:another_file", kwargs={"slug": slug})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=another_content,
            basename=another_name,
            mime_type="text/plain",
        )


class DeserializedBasenameTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        "'deserialized_basename' streams Document.file with custom basename."
        setup_document()
        url = reverse("object:deserialized_basename", kwargs={"slug": slug})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=file_content,
            basename=basename,
            mime_type="text/plain",
        )


class InlineFileTestCase(django.test.TestCase):
    @temporary_media_root()
    def test_download_response(self):
        "'inline_file_view' streams Document.file inline."
        setup_document()
        url = reverse("object:inline_file", kwargs={"slug": slug})
        response = self.client.get(url)
        assert_download_response(
            self,
            response,
            content=file_content,
            mime_type="text/plain",
            attachment=False,
        )
