from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Header(BasePage):
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    def get_cart_count(self):
        if not self.is_visible(self.CART_BADGE, timeout=1):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def open_cart(self):
        self.click(self.CART_LINK)

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)
