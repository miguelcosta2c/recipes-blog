from .base import AuthorsBaseTest
from utils.browser import quit_browser

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def form_field_test_with_callback(self, browser: WebDriver, callback):
        browser.get(self.a_register_url)
        form = self.get_form_from_browser(browser)
        self.fill_form_dummy_data(form)
        callback(browser, form)

    @quit_browser()
    def test_authors_first_name_cannot_be_empty_on_register(
        self, browser: WebDriver
    ):
        def callback(browser, form):
            first_name_field = self.get_element_by_placeholder(
                form, 'Ex: John...')
            self.clear_and_send(first_name_field, ' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('First name cannot be empty', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_username_cannot_be_empty_on_register(
        self, browser: WebDriver
    ):
        def callback(browser, form):
            first_name_field = self.get_element_by_placeholder(
                form, 'Ex: John...')
            self.clear_and_send(first_name_field, ' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Username cannot be empty', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_last_name_cannot_be_empty_on_register(
        self, browser: WebDriver
    ):
        def callback(browser, form):
            last_name_field = self.get_element_by_placeholder(
                form, 'Ex: Doe...')
            self.clear_and_send(last_name_field, ' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Last name cannot be empty', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_password_cannot_be_empty_on_register(
        self, browser: WebDriver
    ):
        def callback(browser, form):
            password_field = self.get_element_by_placeholder(
                form, 'Password...')
            self.clear_and_send(password_field, ' '*8)
            password_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Password cannot be empty', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_password2_cannot_be_empty_on_register(
        self, browser: WebDriver
    ):
        def callback(browser, form):
            password2_field = self.get_element_by_placeholder(
                form, 'Repeat your password...')
            self.clear_and_send(password2_field, ' ')
            password2_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Please repeat your password', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_invalid_email_error(self, browser: WebDriver):
        def callback(browser, form):
            email_field = self.get_element_by_placeholder(form, 'E-mail...')
            self.clear_and_send(email_field, 'email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Enter a valid email address.', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_authors_passwords_dont_match(self, browser: WebDriver):
        def callback(browser, form):
            password1 = self.get_element_by_placeholder(form, 'Password...')
            password2 = self.get_element_by_placeholder(form, 'Repeat your password...')  # noqa: E501
            self.clear_and_send(password1, 'P4ssw@rd')
            self.clear_and_send(password2, 'P4ssw@rd_different')
            password1.send_keys(Keys.ENTER)
            form = self.get_form_from_browser(browser)
            self.assertIn('Passwords must be the same', form.text)
        self.form_field_test_with_callback(browser, callback)

    @quit_browser()
    def test_user_valid_data_register_successfully(self, browser: WebDriver):
        browser.get(self.a_register_url)
        form = self.get_form_from_browser(browser)
        fields = [
            ('Username...', 'username'),
            ('E-mail...', 'user@email.com'),
            ('Ex: John...', 'First Name'),
            ('Ex: Doe...', 'Last Name'),
            ('Password...', 'P4ssw@rd'),
            ('Repeat your password...', 'P4ssw@rd')
        ]
        for field, text in fields:
            self.get_element_by_placeholder(form, field).send_keys(text)
        form.submit()
        self.assertIn(
            'User has been registered, please log in',
            browser.find_element(By.TAG_NAME, 'body').text
        )
