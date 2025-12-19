from __future__ import annotations
from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect

from src.main.ui.data.users import UserCredConfiguration
from src.main.ui.pages.base_page import BasePage
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.catalog_page import CatalogPage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.page.get_by_placeholder("Username")
        self.password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.locator("#login-button")
        self.error_message = self.page.locator('[data-test="error"]')

    def open(self) -> "LoginPage":
        with allure.step("Open Login page"):
            self.page.goto(self.URL)
        return self

    def should_be_opened(self) -> "LoginPage":
        expect(self.login_button).to_be_visible()
        return self

    # --- общий приватный шаг отправки формы ---
    def _submit_login(self, user_creds: UserCredConfiguration) -> None:
        self.fill(self.username_input, user_creds.username)
        self.fill(self.password_input, user_creds.password)
        self.click(self.login_button)

    # --- позитивный логин: возвращаем CatalogPage ---
    def login_success(self, user_creds: UserCredConfiguration) -> "CatalogPage":
        with allure.step(f"Login as '{user_creds.username}' (success)"):
            self._submit_login(user_creds)
        from src.main.ui.pages.catalog_page import CatalogPage
        return self.get_page(CatalogPage)  # ready=True → вызовет CatalogPage.should_be_opened()

    # --- негативный логин: остаёмся на LoginPage ---
    def login_fail(self, user_creds: UserCredConfiguration) -> "LoginPage":
        with allure.step(f"Login as '{user_creds.username}' (fail)"):
            self._submit_login(user_creds)
        return self

    def should_have_error(self, text: str) -> "LoginPage":
        with allure.step(f"Ошибка при логине: {text}"):
            expect(self.error_message).to_contain_text(text)
        return self
