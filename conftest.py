import os

import allure
import pytest
from selenium import webdriver

from utils.config_reader import CONFIG


def _is_headless():
    return os.getenv("HEADLESS", str(CONFIG.get("headless", False))).lower() == "true"


def _build_driver():
    browser = os.getenv("BROWSER", CONFIG.get("browser", "chrome")).lower()
    headless = _is_headless()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-features=PasswordLeakDetection")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
        return webdriver.Chrome(options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {browser}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request):
    driver = _build_driver()
    driver.get(CONFIG["base_url"])
    yield driver

    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"{request.node.name}_failure",
            attachment_type=allure.attachment_type.PNG,
        )
    driver.quit()

