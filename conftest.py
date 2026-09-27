import os
from datetime import datetime

import pytest
from selenium import webdriver

from utils.config_reader import CONFIG, ROOT_DIR

SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "reports", "screenshots")


def _browser_name():
    return os.getenv("BROWSER", CONFIG.get("browser", "chrome")).lower()


def _is_headless():
    return os.getenv("HEADLESS", str(CONFIG.get("headless", False))).lower() == "true"


def _build_driver():
    browser = _browser_name()
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
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        file_name = f"{request.node.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, file_name))
    driver.quit()
