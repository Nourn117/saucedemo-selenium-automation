import json
import os
import platform
import shutil

import allure
import pytest
import selenium
from selenium import webdriver

from utils.config_reader import CONFIG, ROOT_DIR

_run_info = {}


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
    _run_info["browser_version"] = driver.capabilities.get("browserVersion", "unknown")
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


def _write_environment(results_dir):
    environment = {
        "Browser": _browser_name().capitalize(),
        "Browser.Version": _run_info.get("browser_version", "unknown"),
        "Headless": str(_is_headless()),
        "Base.URL": CONFIG["base_url"],
        "Python.Version": platform.python_version(),
        "Selenium.Version": selenium.__version__,
        "OS": f"{platform.system()} {platform.release()}",
    }
    with open(os.path.join(results_dir, "environment.properties"), "w", encoding="utf-8") as file:
        for key, value in environment.items():
            file.write(f"{key}={value}\n")


def _write_executor(results_dir):
    if os.getenv("GITHUB_ACTIONS") != "true":
        return
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    owner, _, name = repo.partition("/")
    run_number = os.getenv("GITHUB_RUN_NUMBER", "0")
    executor = {
        "name": "GitHub Actions",
        "type": "github",
        "buildName": f"Run #{run_number}",
        "buildOrder": int(run_number),
        "buildUrl": f"{server}/{repo}/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}",
        "reportUrl": f"https://{owner.lower()}.github.io/{name}/",
        "reportName": "SauceDemo Allure Report",
    }
    with open(os.path.join(results_dir, "executor.json"), "w", encoding="utf-8") as file:
        json.dump(executor, file, indent=2)


def _copy_categories(results_dir):
    source = os.path.join(ROOT_DIR, "config", "allure_categories.json")
    if os.path.exists(source):
        shutil.copy(source, os.path.join(results_dir, "categories.json"))


def pytest_sessionfinish(session):
    if hasattr(session.config, "workerinput"):
        return
    results_dir = session.config.getoption("allure_report_dir", None)
    if not results_dir:
        return
    os.makedirs(results_dir, exist_ok=True)
    _write_environment(results_dir)
    _write_executor(results_dir)
    _copy_categories(results_dir)
