from __future__ import annotations
from typing import TYPE_CHECKING
from playwright.sync_api import Page
from src.main.ui.pages.base_page import BasePage
from src.main.ui.components.header import Header
import allure

if TYPE_CHECKING:
    from src.main.ui.pages.login_page import LoginPage
    from src.main.ui.pages.basket_page import BasketPage


class BaseAuthedPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)

    def should_cart_badge_be(self, count: int) -> "BaseAuthedPage":
        with allure.step(f"Verify cart badge = {count}"):
            self.header.should_cart_badge_be(count)
        return self

    def logout(self) -> "LoginPage":
        with allure.step("Logout"):
            self.header.logout()
        from src.main.ui.pages.login_page import LoginPage
        return self.get_page(LoginPage)

    def open_cart(self) -> "BasketPage":
        with allure.step("Open cart"):
            self.header.open_cart()
        from src.main.ui.pages.basket_page import BasketPage
        return self.get_page(BasketPage)
