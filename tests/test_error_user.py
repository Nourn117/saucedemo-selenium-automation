import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.header import Header
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.products import BACKPACK
from utils.config_reader import CONFIG


@allure.title("AUT-019: Error user completes checkout")
@allure.suite("TS-07 Error User Defects")
@allure.issue("BUG-010")
@pytest.mark.defect
@pytest.mark.xfail(reason="BUG-010")
def test_error_user_finish(driver):
    LoginPage(driver).login(CONFIG["users"]["error"], CONFIG["password"])
    InventoryPage(driver).add_to_cart(BACKPACK)
    Header(driver).open_cart()
    CartPage(driver).checkout()

    info = CheckoutInfoPage(driver)
    info.fill_info("Amira", "Ashraf", "12345")
    info.continue_checkout()

    overview = CheckoutOverviewPage(driver)
    assert overview.get_item_total() == 29.99
    assert overview.get_tax() == 2.40
    assert overview.get_total() == 32.39

    overview.finish()
    assert CheckoutCompletePage(driver).is_displayed(), "Checkout: Complete page was not displayed after Finish"
