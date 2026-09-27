import pytest


@pytest.mark.smoke
def test_site_opens(driver):
    assert driver.title == "Swag Labs"
