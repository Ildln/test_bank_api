from __future__ import annotations

from typing import TYPE_CHECKING
from src.main.ui.models.product_info import ProductInfo
from src.main.ui.pages.base_auth_page import BaseAuthedPage
from playwright.sync_api import Page, expect
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.product_details import ProductDetailsPage



class CatalogPage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.catalog_items = self.page.locator(".inventory_item")
        self.product_sort = self.page.locator(".product_sort_container")
        self.cart_badge = self.page.locator(".shopping_cart_badge")

    # --- Маркер страницы (готовность) ---
    def should_be_opened(self):
        expect(self.catalog_items.first).to_be_visible()
        return self

    # --- Сортировка ---
    def items_sort(self, value: str):
        with allure.step(f"Sort items: '{value}'"):
            self.product_sort.select_option(value)
        return self

    # --- Действия с корзиной из каталога (по карточке товара) ---
    def add_to_cart(self, product_name: str):
        with allure.step(f"Add to cart: {product_name}"):
            card = self.catalog_items.filter(has_text=product_name).first
            add_button = card.get_by_role("button", name="Add to cart")
            if add_button.count() > 0:
                add_button.click()
        return self

    def remove_from_cart(self, product_name: str):
        with allure.step(f"Remove from cart: {product_name}"):
            card = self.catalog_items.filter(has_text=product_name).first
            remove_button = card.get_by_role("button", name="Remove")
            if remove_button.count() > 0:
                remove_button.click()
        return self

    def add_items_to_cart(self, items: list[str]) -> "CatalogPage":
        for name in items:
            self.add_to_cart(name)
        return self

    # --- Проверки UI-состояния карточки товара ---
    def should_item_button_show_remove(self, product_name: str):
        card = self.catalog_items.filter(has_text=product_name).first
        self.should_be_visible(card.get_by_role("button", name="Remove"))
        return self

    def should_item_button_show_add_to_cart(self, product_name: str):
        card = self.catalog_items.filter(has_text=product_name).first
        self.should_be_visible(card.get_by_role("button", name="Add to cart"))
        return self

    # --- Геттеры (данные для тестов) ---
    def get_product_count(self) -> int:
        return self.catalog_items.count()

    def get_product_name(self) -> list[str]:
        return self.catalog_items.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices_text = self.catalog_items.locator(".inventory_item_price").all_text_contents()
        return [self.parse_price(p) for p in prices_text]

    def get_info_from_card(self, product_name: str) -> ProductInfo:
        card = self.catalog_items.filter(has_text=product_name).first
        name = card.locator(".inventory_item_name").inner_text()
        price = self.parse_price(card.locator(".inventory_item_price").inner_text())
        return ProductInfo(name=name, price=price)

    # --- Навигация. Переход на страницу деталей товара ---
    def open_product_details(self, product_name: str) -> ProductDetailsPage:
        with allure.step(f"Open product details: {product_name}"):
            self.catalog_items.filter(has_text=product_name).locator(".inventory_item_name").first.click()
        from src.main.ui.pages.product_details import ProductDetailsPage
        return self.get_page(ProductDetailsPage)
