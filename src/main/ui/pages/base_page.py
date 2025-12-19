import allure
from abc import ABC
from typing import Type, TypeVar
from playwright.sync_api import Page, Locator, expect

T = TypeVar("T", bound="BasePage")

class BasePage(ABC):

    def __init__(self, page: Page):
        self.page = page

    def get_page(self, page_class: Type[T], *, ready: bool = True) -> T:
        obj =  page_class(self.page)
        if ready:
            obj.should_be_opened()
        return obj

    def click(self, locator: Locator):
        locator.click()
        return self

    def fill(self, locator: Locator, value: str):
        locator.fill(value)
        return self

    def should_be_visible(self, locator: Locator):
        expect(locator).to_be_visible()
        return self

    def should_have_url(self, url: str):
        expect(self.page).to_have_url(url)
        return self

    @staticmethod
    def parse_price(text: str) -> float:
        return float(text.split("$")[-1].strip())

    def screenshot(self, name: str):
        png = self.page.screenshot(full_page=True)
        allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
        return self