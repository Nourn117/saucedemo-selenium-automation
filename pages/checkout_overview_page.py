from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    @staticmethod
    def _amount(text):
        return float(text.split("$")[-1])

    def is_displayed(self):
        return "checkout-step-two.html" in self.current_url

    def get_item_names(self):
        if not self.is_visible(self.CART_ITEMS, timeout=1):
            return []
        return [element.text for element in self.find_all(self.ITEM_NAME)]

    def get_item_prices(self):
        if not self.is_visible(self.CART_ITEMS, timeout=1):
            return []
        return [self._amount(element.text) for element in self.find_all(self.ITEM_PRICE)]

    def get_item_total(self):
        return self._amount(self.get_text(self.ITEM_TOTAL))

    def get_tax(self):
        return self._amount(self.get_text(self.TAX))

    def get_total(self):
        return self._amount(self.get_text(self.TOTAL))

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
