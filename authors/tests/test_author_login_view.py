from django.test import TestCase
from django.urls import reverse


class LoginViewTest(TestCase):
    def test_register_view_get_returns_404(self):
        url = reverse('authors:authenticate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
