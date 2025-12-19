import allure
import pytest

from src.main.ui.data.items import Items, ItemSets
from src.main.ui.data.messages import Message

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Basket")]


def test_add_item_and_check_in_cart(logged_in_catalog):
    product_name = Items.BACKPACK
    (
        logged_in_catalog
            .add_to_cart(product_name)
            .open_cart()
            .expect_item_in_cart(product_name)
    )

def test_add_items_and_check_in_cart(logged_in_catalog):
    items = ItemSets.TWO

    (
        logged_in_catalog
            .add_to_cart(items[0])
            .add_to_cart(items[1])
            .open_cart()
            .expect_items_in_cart(items)
    )


def test_remove_item_from_cart(logged_in_catalog):
    product_name = Items.FLEECE_JACKET

    (
        logged_in_catalog
            .add_to_cart(product_name)
                .open_cart()
                .expect_item_in_cart(product_name)
                .remove_item(product_name)
                .expect_item_not_in_cart(product_name)
    )

def test_remove_items_from_cart(logged_in_catalog):
    items = ItemSets.TWO

    (
        logged_in_catalog
            .add_items_to_cart(items)
                .open_cart()
                .expect_items_in_cart(items)
                .remove_items(*items)
                .expect_cart_empty()
    )

def test_2_remove_items_from_cart(logged_in_catalog):
    items = ItemSets.TWO

    (
        logged_in_catalog
            .add_items_to_cart(items)
                .open_cart()
                .expect_items_in_cart(items)
                .remove_item(items[1])
                .expect_item_not_in_cart(items[1])
                .expect_item_in_cart(items[0])

    )

def test_3_remove_items_from_cart(logged_in_catalog):
    items = ItemSets.THREE

    (
        logged_in_catalog
            .add_items_to_cart(items)
                .open_cart()
                .expect_items_in_cart(items)
                .remove_items(items[1], items[2])
                .expect_items_not_in_cart(items[1], items[2])
                .expect_item_in_cart(items[0])

    )

@allure.title("End-2-End тест")
def test_checkout_multiple_items(logged_in_catalog, attach_screenshot):
    items = ItemSets.E2E_CHECKOUT

    basket_page = (
        logged_in_catalog
            .add_items_to_cart(items)
            .open_cart()
                .expect_items_in_cart(items)
    )

    attach_screenshot("Корзина: добавленные предметы")
    expected_total = basket_page.get_items_total_price()

    (
        basket_page
        .checkout()
            .input_info("ass", "asd", "sdfsd")
            .screenshot("Скрин страницы оформелния заказа, поля")
            .continue_click()
                .should_item_total_be(expected_total)
                .should_total_equal_item_total_plus_tax()
                .finish_click()
                    .should_have_success_message(Message.ORDER_SUCCESS)
                    .screenshot("Проверяем страницу конца покупки")
                    .back_home_click()
    )

def test_checkout_without_postal_code(logged_in_catalog):
    product_name = Items.FLEECE_JACKET

    (
        logged_in_catalog
            .add_to_cart(product_name)
            .open_cart()
                .expect_item_in_cart(product_name)
                .checkout()
                    .input_info("asd", "asd", "")
                    .continue_expect_error()
                    .should_have_error_text(Message.CHECKOUT_POSTAL_REQUIRED)
    )
