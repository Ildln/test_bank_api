from __future__ import annotations

from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect
from src.main.ui.pages.base_auth_page import BaseAuthedPage
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.catalog_page import CatalogPage

class CheckoutCompletePage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.message = self.page.locator(".complete-header")
        self.back_home_button = self.page.locator("#back-to-products")

    # --- Проверка готовности страницы перед переходом. ready = True ---
    def should_be_opened(self) -> "CheckoutCompletePage":
        expect(self.title).to_have_text("Checkout: Complete!")
        expect(self.back_home_button).to_be_visible()
        return self

    # --- Проверки: сообщения ---
    def should_have_success_message(self, text: str) -> "CheckoutCompletePage":
        with allure.step(f"Verify success message contains: '{text}'"):
            expect(self.message).to_contain_text(text)
        return self

    # --- Действия --
    def back_home_click(self) -> "CatalogPage":
        with allure.step("Back home (to catalog)"):
            self.back_home_button.click()
        from src.main.ui.pages.catalog_page import CatalogPage
        return self.get_page(CatalogPage)
