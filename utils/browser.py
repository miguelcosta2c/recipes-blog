from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

from typing import Callable
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_DIR / 'bin' / CHROMEDRIVER_NAME


class BrowserException(Exception):
    ...


def make_chrome_browser(*options, headless: bool | None = None):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if headless is True:
        chrome_options.add_argument('--headless')

    if os.environ.get('NOT_SHOWS_BROWSER') == '1' and headless is None:
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(
        options=chrome_options,
        service=chrome_service
    )
    return browser


def quit_browser(
    *options,
    func_browser: Callable[..., WebDriver] = make_chrome_browser,
    time_to_close: int | None = None,
    headless: bool | None = None
):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            browser = func_browser(*options, headless=headless)
            try:
                func(browser=browser, *args, **kwargs)
            except Exception as e:
                print('ERROR!')
                raise BrowserException(e)
            else:
                if time_to_close:
                    sleep(int(time_to_close))
                browser.quit()
        return _wrapper
    return _decorator


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('http://www.google.com/')
    sleep(5)
    browser.quit()
