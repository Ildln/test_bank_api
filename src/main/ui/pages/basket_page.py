from __future__ import annotations

from typing import TYPE_CHECKING
from src.main.ui.pages.base_auth_page import BaseAuthedPage
from playwright.sync_api import Page, expect, Locator
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.checkout_info_page import CheckoutInfoPage


class BasketPage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        self.item_cart = self.page.locator(".cart_item")
        self.checkout_button = self.page.locator("#checkout")

    @property
    def item_names(self) -> Locator:
        return self.item_cart.locator(".inventory_item_name")

    @property
    def item_prices(self) -> Locator:
        return self.item_cart.locator(".inventory_item_price")

    # --- Проверка готовности страницы перед переходом. ready = True ---
    def should_be_opened(self) -> "BasketPage":
        expect(self.title).to_have_text("Your Cart")
        expect(self.checkout_button).to_be_visible()
        return self

    # --- Переход ---
    def checkout(self) -> "CheckoutInfoPage":
        with allure.step("Go to checkout"):
            self.checkout_button.click()
        from src.main.ui.pages.checkout_info_page import CheckoutInfoPage
        return self.get_page(CheckoutInfoPage)

    # --- Удаление ---
    def remove_item(self, product_name: str) -> "BasketPage":
        with allure.step(f"Remove item from cart: {product_name}"):
            card = self.item_cart.filter(has_text=product_name).first
            button = card.get_by_role("button", name="Remove").first
            if button.count() > 0:
                button.click()
        return self

    def remove_items(self, *items: str) -> "BasketPage":
        for name in items:
            self.remove_item(name)
        return self

    # --- Проверки: добавления --
    def expect_item_in_cart(self, product_name: str) -> "BasketPage":
        """Проверяем, что товар присутствует в корзине"""
        expect(self.item_names).to_contain_text(product_name)
        cart_item_name = self.item_names.all_text_contents()
        assert product_name in cart_item_name, f"{product_name} не найден, есть: {cart_item_name}"
        return self

    def expect_items_in_cart(self, items: list[str]) -> "BasketPage":
        """Проверяем, что товары присутствует в корзине"""
        expect(self.item_names).to_have_count(len(items))
        cart_names = self.item_names.all_text_contents()
        assert set(cart_names) == set(items), f"Ожидали {items}, получили {cart_names}"
        return self

    # --- Проверки: удаления --
    def expect_item_not_in_cart(self, product_name: str) -> "BasketPage":
        """Проверяем, что товар отсутствует в корзине"""
        expect(self.item_cart.filter(has_text=product_name)).to_have_count(0)
        return self

    def expect_items_not_in_cart(self, *items: str) -> "BasketPage":
        """Проверяем, что перечисленные товары отсутствует в корзине"""
        for name in items:
            self.expect_item_not_in_cart(name)
        return self

    def expect_cart_empty(self) -> "BasketPage":
        """Проверяем, что корзина полностью пустая"""
        expect(self.item_cart).to_have_count(0)
        return self

    # --- Геттеры (данные для тестов) ---
    def get_item_names(self) -> list[str]:
        return self.item_names.all_text_contents()

    def get_item_prices(self) -> list[float]:
        price_text = self.item_prices.all_text_contents()
        return [self.parse_price(p) for p in price_text]

    def get_items_total_price(self) -> float:
        prices_text = self.item_prices.all_text_contents()
        return sum(self.parse_price(p) for p in prices_text)