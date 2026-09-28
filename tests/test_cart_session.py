import allure
import pytest

from pages.header import Header
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.side_menu import SideMenu
from test_data.products import ONESIE, RED_TSHIRT
from utils.config_reader import CONFIG


@allure.title("AUT-025: Cart does not persist across users")
@allure.suite("TS-06 Cart & Session Defects")
@allure.issue("BUG-014")
@pytest.mark.defect
@pytest.mark.xfail(reason="BUG-014")
def test_cart_not_shared_between_users(driver):
    LoginPage(driver).login(CONFIG["users"]["standard"], CONFIG["password"])
    inventory = InventoryPage(driver)
    inventory.add_to_cart(ONESIE)
    inventory.add_to_cart(RED_TSHIRT)
    assert Header(driver).get_cart_count() == 2

    SideMenu(driver).logout()
    LoginPage(driver).login(CONFIG["users"]["error"], CONFIG["password"])

    count = Header(driver).get_cart_count()
    assert count == 0, f"error_user sees {count} items left by standard_user"
