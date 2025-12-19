from __future__ import annotations

from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect
from src.main.ui.pages.base_auth_page import BaseAuthedPage
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInfoPage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.input_first_name = self.page.get_by_placeholder("First Name")
        self.input_last_name = self.page.get_by_placeholder("Last Name")
        self.input_postal_code = self.page.get_by_placeholder("Zip/Postal Code")
        self.cancel_button = self.page.locator("#cancel")
        self.continue_button = self.page.locator("#continue")
        self.error_message = self.page.locator("h3[data-test='error']")

    # --- Проверка готовности страницы перед переходом. ready = True ---
    def should_be_opened(self) -> "CheckoutInfoPage":
        expect(self.title).to_have_text("Checkout: Your Information")
        expect(self.continue_button).to_be_visible()
        return self

    # --- Действия и навигация --
    def input_info(self, first_name: str, last_name: str, code: str) -> "CheckoutInfoPage":
        with allure.step("Заполняем поля"):
            self.fill(self.input_first_name, first_name)
            self.fill(self.input_last_name, last_name)
            self.fill(self.input_postal_code, code)
        return self

    def continue_click(self) -> "CheckoutOverviewPage":
        with allure.step("Click Continue"):
            self.click(self.continue_button)
        from src.main.ui.pages.checkout_overview_page import CheckoutOverviewPage
        return self.get_page(CheckoutOverviewPage)

    def continue_expect_error(self) -> "CheckoutInfoPage":
        with allure.step("Click Continue (expect error)"):
            self.click(self.continue_button)
        return self

    # --- Проверка ---
    def should_have_error_text(self, text: str) -> "CheckoutInfoPage":
        expect(self.error_message).to_contain_text(text)
        return self