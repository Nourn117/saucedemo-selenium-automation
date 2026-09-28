from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class InventoryPage(BasePage):
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGE = (By.CSS_SELECTOR, "img.inventory_item_img")
    ITEM_BUTTON = (By.CSS_SELECTOR, "button")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    SORT_OPTIONS = {
        "Name (A to Z)": "az",
        "Name (Z to A)": "za",
        "Price (low to high)": "lohi",
        "Price (high to low)": "hilo",
    }

    def is_displayed(self):
        return "inventory.html" in self.current_url and self.is_visible(self.ITEMS)

    def _get_item(self, product_name):
        for item in self.find_all(self.ITEMS):
            if item.find_element(*self.ITEM_NAME).text == product_name:
                return item
        raise ValueError(f"Product not found: {product_name}")

    def add_to_cart(self, product_name):
        button = self._get_item(product_name).find_element(*self.ITEM_BUTTON)
        if button.text.strip().lower() == "add to cart":
            button.click()

    def remove_from_cart(self, product_name):
        button = self._get_item(product_name).find_element(*self.ITEM_BUTTON)
        if button.text.strip().lower() == "remove":
            button.click()

    def add_all_to_cart(self):
        for name in self.get_product_names():
            self.add_to_cart(name)

    def get_button_text(self, product_name):
        return self._get_item(product_name).find_element(*self.ITEM_BUTTON).text

    def open_product(self, product_name):
        self._get_item(product_name).find_element(*self.ITEM_NAME).click()

    def get_product_names(self):
        return [element.text for element in self.find_all(self.ITEM_NAME)]

    def get_product_prices(self):
        return [float(element.text.replace("$", "")) for element in self.find_all(self.ITEM_PRICE)]

    def get_product_price(self, product_name):
        price = self._get_item(product_name).find_element(*self.ITEM_PRICE).text
        return float(price.replace("$", ""))

    def get_prices_by_name(self):
        return dict(zip(self.get_product_names(), self.get_product_prices()))

    def get_image_sources(self):
        return [element.get_attribute("src") for element in self.find_all(self.ITEM_IMAGE)]

    def get_image_source(self, product_name):
        return self._get_item(product_name).find_element(*self.ITEM_IMAGE).get_attribute("src")

    def sort_by(self, option_text):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(self.SORT_OPTIONS[option_text])

    def get_selected_sort(self):
        return Select(self.find(self.SORT_DROPDOWN)).first_selected_option.text

    def get_alert_text_and_accept(self, timeout=2):
        """Returns the text of a JS alert if one appears, otherwise None."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        text = alert.text
        alert.accept()
        return text
