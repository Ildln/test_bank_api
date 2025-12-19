from __future__ import annotations
from playwright.sync_api import Page, expect


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.menu_btn_close = self.page.locator("#react-burger-cross-btn")

    def open_menu(self) -> "Header":
        self.menu_btn.click()
        return self

    def close_menu(self) -> "Header":
        if self.menu_btn_close.is_visible():
            self.menu_btn_close.click()
        return self

    def logout(self) -> "Header":
        self.open_menu()
        self.logout_link.click()
        return self

    def open_cart(self) -> "Header":
        self.cart_link.click()
        return self

    def should_cart_badge_be(self, count: int) -> "Header":
        if count == 0:
            expect(self.cart_badge).to_have_count(0)
        else:
            expect(self.cart_badge).to_have_text(str(count))
        return self