import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.header import Header
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.products import BACKPACK, BIKE_LIGHT, CATALOG_PRICES, CHECKOUT_INFO, ONESIE, TAX_RATE
from utils.config_reader import CONFIG


def _checkout(driver, products):
    LoginPage(driver).login(CONFIG["users"]["standard"], CONFIG["password"])
    inventory = InventoryPage(driver)
    for product in products:
        inventory.add_to_cart(product)
    assert Header(driver).get_cart_count() == len(products)

    Header(driver).open_cart()
    assert sorted(CartPage(driver).get_item_names()) == sorted(products)
    CartPage(driver).checkout()

    info = CheckoutInfoPage(driver)
    info.fill_info(**CHECKOUT_INFO)
    info.continue_checkout()
    return CheckoutOverviewPage(driver)


@allure.title("AUT-005: Successful end-to-end checkout")
@allure.suite("TS-03 Checkout - Positive")
@pytest.mark.positive
def test_successful_checkout(driver):
    overview = _checkout(driver, [BACKPACK])

    assert overview.get_item_names() == [BACKPACK]
    assert overview.get_item_total() == 29.99
    assert overview.get_tax() == 2.40
    assert overview.get_total() == 32.39

    overview.finish()
    assert CheckoutCompletePage(driver).get_header() == "Thank you for your order!"


@allure.title("AUT-007: Cart total calculation with multiple items")
@allure.suite("TS-03 Checkout - Positive")
@pytest.mark.positive
def test_cart_total_calculation(driver):
    products = [BACKPACK, BIKE_LIGHT, ONESIE]
    overview = _checkout(driver, products)

    expected_item_total = round(sum(CATALOG_PRICES[p] for p in products), 2)
    expected_tax = round(expected_item_total * TAX_RATE, 2)
    expected_total = round(expected_item_total + expected_tax, 2)

    item_total, tax, total = overview.get_item_total(), overview.get_tax(), overview.get_total()
    assert item_total == expected_item_total, f"Item total: expected {expected_item_total}, got {item_total}"
    assert tax == expected_tax, f"Tax: expected {expected_tax}, got {tax}"
    assert total == expected_total, f"Total: expected {expected_total}, got {total}"
