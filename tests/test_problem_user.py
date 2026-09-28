import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.header import Header
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.products import BACKPACK
from utils.config_reader import CONFIG


@allure.title("AUT-011: Problem user checkout flow")
@allure.suite("TS-05 Problem User Defects")
@allure.issue("BUG-001")
@pytest.mark.defect
@pytest.mark.xfail(reason="BUG-001")
def test_problem_user_checkout(driver):
    LoginPage(driver).login(CONFIG["users"]["problem"], CONFIG["password"])
    InventoryPage(driver).add_to_cart(BACKPACK)
    Header(driver).open_cart()
    CartPage(driver).checkout()

    info = CheckoutInfoPage(driver)
    info.enter_first_name("Amira")
    info.enter_last_name("Ashraf")

    assert info.get_first_name_value() == "Amira", f"First Name changed to '{info.get_first_name_value()}'"
    assert info.get_last_name_value() == "Ashraf", f"Last Name is '{info.get_last_name_value()}'"

    info.enter_postal_code("12345")
    info.continue_checkout()
    assert CheckoutOverviewPage(driver).is_displayed()
