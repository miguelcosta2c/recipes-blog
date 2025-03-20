import pytest
from django.contrib.auth.models import User
from utils.browser import quit_browser
from .base import AuthorsBaseTest

from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    @quit_browser()
    def test_valid_user_can_login_successfully(self, browser: WebDriver):
        kwargs = {
            'username': 'my_user',
            'password': 'P4ssw@rd'
        }
        success_message = f'You are logged in with {kwargs["username"]}'
        User.objects.create_user(**kwargs)

        # User opens the browser
        browser.get(self.a_login_url)

        form = self.get_main_form(browser)
        username_field = self.get_element_by_placeholder(form, 'Username...')
        password_field = self.get_element_by_placeholder(form, 'Password...')

        username_field.send_keys(kwargs['username'])
        password_field.send_keys(kwargs['password'])

        form.submit()

        self.assertIn(success_message, self.get_body_text(browser))

    @quit_browser()
    def test_user_loginform_is_valid(self, browser: WebDriver):
        # User opens login page
        browser.get(self.a_login_url)

        # User sees the form
        form = self.get_main_form(browser)

        # And tries to send empty values
        username = self.get_element_by_placeholder(form, 'Username...')
        password = self.get_element_by_placeholder(form, 'Password...')

        username.send_keys(' ')
        password.send_keys(' ')

        # Submits the form
        form.submit()

        # Error message
        self.assertIn('Form invalid credentials', self.get_body_text(browser))

    @quit_browser()
    def test_user_loginform_invalid_credentials_error(self, browser: WebDriver):  # noqa: E501
        # User opens login page
        browser.get(self.a_login_url)

        # User sees the form
        form = self.get_main_form(browser)

        # And tries to send invalid credentials
        username = self.get_element_by_placeholder(form, 'Username...')
        password = self.get_element_by_placeholder(form, 'Password...')

        username.send_keys('invalidsuer')
        password.send_keys('invalidpassword')

        # Submits the form
        form.submit()

        # Error message
        self.assertIn('User invalid Credentials', self.get_body_text(browser))
