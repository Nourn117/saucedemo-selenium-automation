from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_BUTTON = (By.CSS_SELECTOR, "button")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def is_displayed(self):
        return "cart.html" in self.current_url

    def get_item_names(self):
        if not self.is_visible(self.CART_ITEMS, timeout=1):
            return []
        return [element.text for element in self.find_all(self.ITEM_NAME)]

    def get_item_count(self):
        return len(self.get_item_names())

    def remove(self, product_name):
        for item in self.find_all(self.CART_ITEMS):
            if item.find_element(*self.ITEM_NAME).text == product_name:
                item.find_element(*self.ITEM_BUTTON).click()
                return
        raise ValueError(f"Product not in cart: {product_name}")

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
