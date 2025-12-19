from __future__ import annotations

from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect
from src.main.ui.models.product_info import ProductInfo
from src.main.ui.pages.base_auth_page import BaseAuthedPage

if TYPE_CHECKING:
    from src.main.ui.pages.catalog_page import CatalogPage

class ProductDetailsPage(BaseAuthedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.details_name = self.page.locator(".inventory_details_name")
        self.details_price = self.page.locator(".inventory_details_price")
        self.back_button = self.page.locator("[data-test='back-to-products']")

    # --- Геттеры (данные для тестов) ---
    def get_product_info(self) -> ProductInfo:
        name = self.details_name.inner_text()
        price = self.parse_price(self.details_price.inner_text())
        return ProductInfo(name=name, price=price)

    # --- Переходы --
    def back_to_catalog(self) -> "CatalogPage":
        self.click(self.back_button)
        from src.main.ui.pages.catalog_page import CatalogPage
        return self.get_page(CatalogPage)

    # --- Проверка готовности страницы. ready = True ---
    def should_be_opened(self) -> "ProductDetailsPage":
        expect(self.details_name).to_be_visible()
        return self