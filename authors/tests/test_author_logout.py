from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorsLogoutTest(TestCase):
    def test_user_cannot_logout_with_get_method(self):
        kwargs = {
            'username': 'my_user',
            'password': 'my_pass',
        }
        User.objects.create_user(**kwargs)
        self.client.login(**kwargs)

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request',
            response.content.decode()
        )

    def test_user_cannot_logout_with_another_user(self):
        kwargs = {
            'username': 'my_user',
            'password': 'my_pass',
        }
        User.objects.create_user(**kwargs)
        self.client.login(**kwargs)

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user',
                'password': 'another_password',
            },
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode()
        )

    def test_user_can_logout(self):
        kwargs = {
            'username': 'my_user',
            'password': 'my_pass',
        }
        User.objects.create_user(**kwargs)
        self.client.login(**kwargs)

        response = self.client.post(
            reverse('authors:logout'),
            data=kwargs,
            follow=True
        )

        self.assertIn(
            'Logged out successfully',
            response.content.decode()
        )
