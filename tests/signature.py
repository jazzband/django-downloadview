"""
Test signature generation and validation.
"""

import unittest

from django.core.exceptions import PermissionDenied
from django.core.signing import TimestampSigner

from django_downloadview.decorators import _signature_is_valid
from django_downloadview.storage import SignedURLMixin


class TestStorage:
    def url(self, name):
        return "https://example.com/{name}".format(name=name)


class SignedTestStorage(SignedURLMixin, TestStorage):
    pass


class SignatureGeneratorTestCase(unittest.TestCase):
    def test_signed_storage(self):
        """
        django_downloadview.storage.SignedURLMixin adds X-Signature to URLs.
        """

        storage = SignedTestStorage()
        url = storage.url("test")
        self.assertIn("https://example.com/test?X-Signature=", url)


class SignatureValidatorTestCase(unittest.TestCase):
    def test_verify_signature(self):
        """
        django_downloadview.decorators._signature_is_valid returns True on
        valid signatures.
        """

        signer = TimestampSigner()
        request = unittest.mock.MagicMock()

        request.path = "test"
        request.GET = {"X-Signature": signer.sign("test")}

        self.assertIsNone(_signature_is_valid(request))

    def test_verify_signature_invalid(self):
        """
        django_downloadview.decorators._signature_is_valid raises PermissionDenied
        on invalid signatures.
        """

        request = unittest.mock.MagicMock()

        request.path = "test"
        request.GET = {"X-Signature": "not-valid"}

        with self.assertRaises(PermissionDenied):
            _signature_is_valid(request)
