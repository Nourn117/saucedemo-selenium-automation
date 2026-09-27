import allure
import pytest


@allure.title("AUT-001: Site opens with correct title")
@allure.suite("TS-01 Smoke")
@pytest.mark.smoke
def test_site_opens(driver):
    assert driver.title == "Swag Labs"
