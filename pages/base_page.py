from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import CONFIG


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = CONFIG.get("timeout", 10)
        self.wait = WebDriverWait(driver, self.timeout)

    def open(self, path=""):
        self.driver.get(f"{CONFIG['base_url']}/{path}".rstrip("/"))

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def get_value(self, locator):
        return self.find(locator).get_attribute("value")

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text):
        self.wait.until(EC.url_contains(text))

    @property
    def current_url(self):
        return self.driver.current_url
