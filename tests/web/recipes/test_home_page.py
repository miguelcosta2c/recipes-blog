# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import quit_browser

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixin

from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageTest(StaticLiveServerTestCase, RecipeMixin):
    @quit_browser()
    def test_home_page_with_no_recipes(self, browser: WebDriver):
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    @quit_browser()
    def test_recipes_search_can_find_correct_recipes(self, browser: WebDriver):
        recipes = self.make_recipes_in_batch(qtd=5)
        browser.get(self.live_server_url)
        search_input = browser.find_element(
            By.XPATH,
            '//input[@placeholder="Enter a recipe..."]'
        )
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(
            recipes[0].title,
            browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    @quit_browser()
    def test_recipes_home_pagination_buttons(self, browser: WebDriver):
        self.make_recipes_in_batch(qtd=5)
        browser.get(self.live_server_url)
        page2 = browser.find_element(
            By.XPATH,
            '/html/body/main/nav/div/a[2]'
        )
        page2.click()
        self.assertEqual(
            len(browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
