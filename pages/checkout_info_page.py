from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def is_displayed(self):
        return "checkout-step-one.html" in self.current_url

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME, last_name)

    def enter_postal_code(self, postal_code):
        self.enter_text(self.POSTAL_CODE, postal_code)

    def fill_info(self, first_name, last_name, postal_code):
        if first_name:
            self.enter_first_name(first_name)
        if last_name:
            self.enter_last_name(last_name)
        if postal_code:
            self.enter_postal_code(postal_code)

    def get_first_name_value(self):
        return self.get_value(self.FIRST_NAME)

    def get_last_name_value(self):
        return self.get_value(self.LAST_NAME)

    def get_postal_code_value(self):
        return self.get_value(self.POSTAL_CODE)

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)

    def get_error(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)
