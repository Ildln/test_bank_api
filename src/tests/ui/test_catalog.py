import allure
import pytest

from src.main.ui.data.items import Items

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Catalog")]


def test_count_catalog(logged_in_catalog):
    assert logged_in_catalog.get_product_count() == 6

@allure.title("Сортировка по имени")
def test_sorted_by_name(logged_in_catalog):
    logged_in_catalog.items_sort("az")
    names = logged_in_catalog.get_product_name()
    assert names == sorted(names), "Товары не отсортированы A→Z"

    logged_in_catalog.items_sort("za")
    names = logged_in_catalog.get_product_name()
    assert names == sorted(names, reverse=True)

@allure.title("Сортировка по цене")
def test_sort_by_price(logged_in_catalog):
    logged_in_catalog.items_sort("lohi")
    prices = logged_in_catalog.get_product_prices()
    assert prices == sorted(prices)

    logged_in_catalog.items_sort("hilo")
    prices = logged_in_catalog.get_product_prices()
    assert prices == sorted(prices, reverse=True)

def test_add_to_cart(logged_in_catalog):
    product_name = Items.BIKE_LIGHT
    (
        logged_in_catalog.add_to_cart(product_name)
        .should_item_button_show_remove(product_name)
        .should_cart_badge_be(1)
    )

def test_add_to_cart_and_remove(logged_in_catalog):
    product_name = Items.ONESIE
    (
        logged_in_catalog
            .add_to_cart(product_name)
            .should_item_button_show_remove(product_name)
            .should_cart_badge_be(1)
            .remove_from_cart(product_name)
            .should_cart_badge_be(0)
    )

def test_product_details_onesie(logged_in_catalog):
    product_name = Items.ONESIE
    expected_info = logged_in_catalog.get_info_from_card(product_name) # Инфа с каталога
    open_detail_page = logged_in_catalog.open_product_details(product_name)
    actual_info = open_detail_page.get_product_info()    # Инфа из страницы "детали товара"

    assert expected_info == actual_info, f"Информация на странице деталей товара: {actual_info} не совпадает: {expected_info} "

def test_product_detail_jacket(logged_in_catalog):
    product_name = Items.FLEECE_JACKET
    expected_info_from_card = logged_in_catalog.get_info_from_card(product_name)
    open_detail_page = logged_in_catalog.open_product_details(product_name)
    actual_info_item_from_detail = open_detail_page.get_product_info()

    assert expected_info_from_card == actual_info_item_from_detail

def test_remove_item_from_catalog(logged_in_catalog):
    product_name = Items.ALLTHETHINGS_TSHIRT_RED
    (
        logged_in_catalog
            .add_to_cart(product_name)
            .should_item_button_show_remove(product_name)
            .remove_from_cart(product_name)
            .should_item_button_show_add_to_cart(product_name)
    )


