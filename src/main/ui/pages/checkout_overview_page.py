from __future__ import annotations

from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect
from src.main.ui.pages.base_auth_page import BaseAuthedPage
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.checkout_complete_page import CheckoutCompletePage

class CheckoutOverviewPage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.cancel_button = self.page.locator("#cancel")
        self.finish_button = self.page.locator("#finish")
        self.detail_item_name = self.page.locator(".inventory_item_name")
        self.item_total = self.page.locator(".summary_subtotal_label")
        self.total = self.page.locator(".summary_total_label")
        self.tax = self.page.locator(".summary_tax_label")

    # --- Проверка готовности страницы перед переходом. ready = True ---
    def should_be_opened(self) -> "CheckoutOverviewPage":
        expect(self.title).to_have_text("Checkout: Overview")
        expect(self.detail_item_name.first).to_be_visible()
        expect(self.finish_button).to_be_visible()
        return self

    # --- Геттеры (данные для тестов) ---
    def get_item_total(self) -> float:
        return self.parse_price(self.item_total.inner_text())

    def get_total(self) -> float:
        return self.parse_price(self.total.inner_text())

    def get_tax(self) -> float:
        return self.parse_price(self.tax.inner_text())

    # --- Действия --
    def finish_click(self) -> "CheckoutCompletePage":
        with allure.step("Finish checkout"):
            self.finish_button.click()
        from src.main.ui.pages.checkout_complete_page import CheckoutCompletePage
        return self.get_page(CheckoutCompletePage)

    # --- ОСтальные проверки ---
    def should_item_total_be(self, expected_total: float) -> "CheckoutOverviewPage":
        with allure.step(f"Проверяем item total = {expected_total}"):
            actual = self.get_item_total()
            assert actual == expected_total, (
                f"Item total {actual} не совпадает с суммой товаров {expected_total}"
            )
        return self

    def should_total_equal_item_total_plus_tax(self) -> "CheckoutOverviewPage":
        item_total = self.get_item_total()
        tax = self.get_tax()
        total = self.get_total()
        with allure.step(f"Проверяем total: {total} = item_total + tax: {item_total + tax}"):
            assert total == round(item_total + tax, 2), (
                f"Total {total} не совпадает с Item total {item_total} + Tax {tax}"
            )
        return self