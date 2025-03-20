from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


class UtilsMixin:
    def get_body_text(self, browser: WebDriver):
        return browser.find_element(By.TAG_NAME, 'body').text

    def clear_and_send(self, webelement: WebElement, text: str) -> None:
        webelement.clear()
        webelement.send_keys(text)

    def get_element_by_placeholder(
            self, webelement: WebElement, placeholder: str
    ) -> WebElement:
        return webelement.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form: WebElement) -> None:
        input_fields = form.find_elements(By.TAG_NAME, "input")
        for field in input_fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
        email_field = form.find_element(By.ID, 'id_email')
        self.clear_and_send(email_field, 'dummy@email.com')

    def get_form_from_browser(self, browser: WebDriver) -> WebElement:
        return browser.find_element(By.XPATH, '/html/body/main/div/form')

    def get_main_form(self, browser: WebDriver) -> WebElement:
        return browser.find_element(By.CLASS_NAME, 'main-form')


class AuthorsBaseTest(StaticLiveServerTestCase, UtilsMixin):
    def setUp(self) -> None:
        setup = super().setUp()
        # * Authors base url
        self.a_url = self.live_server_url + '/authors/'
        # * Authors register url
        self.a_register_url = self.a_url + 'register/'
        self.a_register_create_url = self.a_register_url + 'create/'
        # * Authors login url
        self.a_login_url = self.a_url + 'login/'
        self.a_login_auth_url = self.a_login_url + 'authenticate/'
        # * Authors logout url
        self.a_logout_url = self.a_url + 'logout/'
        return setup
