import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.products import CATALOG_PRICES
from utils.config_reader import CONFIG


@allure.title("AUT-021: Visual user sees correct prices")
@allure.suite("TS-08 Visual User Defects")
@allure.issue("BUG-011")
@pytest.mark.defect
@pytest.mark.xfail(reason="BUG-011")
def test_visual_user_prices(driver):
    LoginPage(driver).login(CONFIG["users"]["visual"], CONFIG["password"])
    actual_prices = InventoryPage(driver).get_prices_by_name()

    wrong = {name: price for name, price in actual_prices.items() if CATALOG_PRICES.get(name) != price}
    assert not wrong, f"Prices different from the catalog: {wrong}"
