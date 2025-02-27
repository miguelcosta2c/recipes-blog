from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized  # type: ignore
from django.urls import reverse


class AuthorRegisterFormUnit(TestCase):
    @parameterized.expand(
        [
            ('username', 'Username...'),
            ('email', 'E-mail...'),
            ('first_name', 'Ex: John...'),
            ('last_name', 'Ex: Doe...'),
            ('password', 'Password...'),
            ('password2', 'Repeat your password...'),
        ]
    )
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current, placeholder)

    @parameterized.expand(
        [
            ('username', 'Ex: johndoe'),
            ('email', 'Ex: johndoe@email.com'),
        ]
    )
    def test_fields_help_texts(self, field, help_text):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, help_text)

    @parameterized.expand(
        [
            ('username', 'Username'),
            ('email', 'E-mail'),
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
            ('password', 'Password'),
            ('password2', 'Repeat Password'),
        ]
    )
    def test_fields_labels(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, label)


class AuthorRegisterFormIntegration(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'email': 'email@anyemail.com',
            'first_name': 'douglas',
            'last_name': 'souza',
            'password': 'Str0ngP@ssw0rd1',
            'password2': 'Str0ngP@ssw0rd1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username cannot be empty'),
        ('email', 'E-mail cannot be empty'),
        ('first_name', 'First name cannot be empty'),
        ('last_name', 'Last name cannot be empty'),
        ('password', 'Password cannot be empty'),
        ('password2', 'Please repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn(message, response.context['form'].errors.get(field))

    def test_username_field_min_length_4(self):
        field = 'username'
        self.form_data[field] = 'jon'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error = 'Username must be at least 4 characters long'
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get(field))

    def test_username_field_max_length_150(self):
        url = reverse('authors:create')
        field = 'username'
        self.form_data[field] = 'A' * 151
        response = self.client.post(url, data=self.form_data, follow=True)
        error = 'Username must be at most 150 characters long'
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get(field))

    def test_password_field_min_length_8(self):
        field = 'password'
        self.form_data[field] = 'A' * 7
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error = 'Password must be at least 8 characters long'
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get(field))

    def test_password_field_max_length_150(self):
        url = reverse('authors:create')
        field = 'password'
        self.form_data[field] = 'A' * 151
        response = self.client.post(url, data=self.form_data, follow=True)
        error = 'Password must be at most 150 characters long'
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get(field))

    def test_password_field_has_lowercase_uppercase_numbers_and_no_spaces(self):  # noqa: E501
        field = 'password'
        self.form_data[field] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error = (
            'Password must have at least one uppercase, '
            'Password must contain at least one uppercase letter, '
            'one lowercase letter, '
            'and one number, with no spaces.'
        )
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get(field))

        self.form_data[field] = 'StrongPassword1'

        response2 = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(error, response2.content.decode())

    def test_password_and_password_confirmation(self):
        url = reverse('authors:create')
        field = 'password'
        field2 = 'password2'
        self.form_data[field] = 'StrongPassword1'
        self.form_data[field2] = 'StrongPassword2'
        response = self.client.post(url, data=self.form_data, follow=True)
        error = 'Passwords must be the same'
        self.assertIn(error, response.content.decode())
        self.assertIn(error, response.context["form"].errors.get('__all__'))
        self.form_data[field] = 'StrongPassword1'
        self.form_data[field2] = 'StrongPassword1'
        response2 = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(error, response2.content.decode())

    def test_email_field_is_unique(self):
        url = reverse('authors:create')
        self.client.post(url, self.form_data, follow=True)
        response = self.client.post(url, self.form_data, follow=True)
        error = 'Email is already in use'
        self.assertIn(error, response.context["form"].errors.get('email'))
        self.assertIn(error, response.content.decode())

    def test_author_created_can_login(self):
        url = reverse('authors:create')
        self.form_data.update(
            {
                'username': 'testuser',
                'password': '@Bc123456',
                'password2': '@Bc123456'
            }
        )
        self.client.post(url, self.form_data, follow=True)
        authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )
        self.assertTrue(authenticated)
