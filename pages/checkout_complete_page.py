from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    HEADER = (By.CLASS_NAME, "complete-header")
    TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def is_displayed(self, timeout=3):
        return "checkout-complete.html" in self.current_url or self.is_visible(self.HEADER, timeout)

    def get_header(self):
        return self.get_text(self.HEADER)

    def get_text_message(self):
        return self.get_text(self.TEXT)

    def back_home(self):
        self.click(self.BACK_HOME_BUTTON)
