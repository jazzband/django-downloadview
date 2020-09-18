"""Test suite for demoproject.download."""
from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):
    """Test homepage."""

    def test_get(self):
        """Homepage returns HTTP 200."""
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
