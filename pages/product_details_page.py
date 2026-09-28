from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    NAME = (By.CLASS_NAME, "inventory_details_name")
    PRICE = (By.CLASS_NAME, "inventory_details_price")
    DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    IMAGE = (By.CSS_SELECTOR, "img.inventory_details_img")
    ADD_OR_REMOVE_BUTTON = (By.CSS_SELECTOR, ".inventory_details_desc_container button")
    BACK_BUTTON = (By.ID, "back-to-products")

    def get_name(self):
        return self.get_text(self.NAME)

    def get_price(self):
        return float(self.get_text(self.PRICE).replace("$", ""))

    def get_description(self):
        return self.get_text(self.DESCRIPTION)

    def get_image_source(self):
        return self.find(self.IMAGE).get_attribute("src")

    def get_button_text(self):
        return self.get_text(self.ADD_OR_REMOVE_BUTTON)

    def add_to_cart(self):
        if self.get_button_text().strip().lower() == "add to cart":
            self.click(self.ADD_OR_REMOVE_BUTTON)

    def back_to_products(self):
        self.click(self.BACK_BUTTON)
