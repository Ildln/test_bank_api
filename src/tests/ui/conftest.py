import allure
import pytest

from playwright.sync_api import sync_playwright

from src.main.ui.data.users import UsersCred
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def logged_in_catalog(page) -> CatalogPage:
    return(
        LoginPage(page)
            .open()
            .login_success(UsersCred.STANDARD)
    )

@pytest.fixture
def attach_screenshot(page):
    def _attach(name: str):
        png = page.screenshot(full_page=True)
        allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
    return _attach

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    # Скрины/HTML прикрепляем только если тест упал
    if rep.failed:
        try:
            png = page.screenshot(full_page=True)
            allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

        try:
            html = page.content()
            allure.attach(html, name="page.html", attachment_type=allure.attachment_type.HTML)
        except Exception:
            pass

        try:
            allure.attach(page.url, name="url", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass