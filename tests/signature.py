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


def signable_test_view(request):
    return True


class SignatureGeneratorTestCase(unittest.TestCase):
    def test_signed_storage(self):
        """
        django_downloadview.storage.SignedURLMixin adds X-Signature to URLs.
        """

        storage = SignedTestStorage()
        url = storage.url("test")
        self.assertIn("https://example.com/test?X-Signature=", url)


class SignatureValidatorTestCase(unittest.TestCase):
    def test_signature_required(self):
        """
        django_downloadview.decorators.signature_required 
        wraps view-like callables and returns their values.
        """

        signer = TimestampSigner()
        request = unittest.mock.MagicMock()

        request.path = "test"
        request.GET = {"X-Signature": signer.sign("test")}
        
        response = signature_required(signable_test_view)(request)

        self.assertTrue(response)
        
    def test_signature_is_valid(self):
        """
        django_downloadview.decorators._signature_is_valid 
        returns None on valid signatures.
        """

        signer = TimestampSigner()
        request = unittest.mock.MagicMock()

        request.path = "test"
        request.GET = {"X-Signature": signer.sign("test")}

        self.assertIsNone(_signature_is_valid(request))

    def test_signature_is_valid_error(self):
        """
        django_downloadview.decorators._signature_is_valid 
        raises PermissionDenied on invalid signatures.
        """

        request = unittest.mock.MagicMock()

        request.path = "test"
        request.GET = {"X-Signature": "not-valid"}

        with self.assertRaises(PermissionDenied):
            _signature_is_valid(request)
