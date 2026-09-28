import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.side_menu import SideMenu
from test_data.products import ACCEPTED_USERS
from utils.config_reader import CONFIG


@allure.title("AUT-004: Data-driven login for all accepted users")
@allure.suite("TS-02 Login")
@pytest.mark.positive
@pytest.mark.parametrize("username", ACCEPTED_USERS)
def test_login_all_users(driver, username):
    LoginPage(driver).login(username, CONFIG["password"])
    assert InventoryPage(driver).is_displayed(), f"{username} did not reach the Products page"

    SideMenu(driver).logout()
    assert LoginPage(driver).is_displayed(), f"{username} was not returned to the login page after logout"
