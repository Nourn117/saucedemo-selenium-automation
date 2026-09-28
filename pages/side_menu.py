from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SideMenu(BasePage):
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    ALL_ITEMS = (By.ID, "inventory_sidebar_link")
    ABOUT = (By.ID, "about_sidebar_link")
    LOGOUT = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE = (By.ID, "reset_sidebar_link")

    def open(self):
        self.click(self.MENU_BUTTON)

    def close(self):
        self.click(self.CLOSE_BUTTON)

    def go_to_all_items(self):
        self.open()
        self.click(self.ALL_ITEMS)

    def go_to_about(self):
        self.open()
        self.click(self.ABOUT)

    def logout(self):
        self.open()
        self.click(self.LOGOUT)

    def reset_app_state(self):
        self.open()
        self.click(self.RESET_APP_STATE)
        self.close()

    def click_item(self, link_text):
        """Open the menu and click any item by its visible text, like 'Dynamic Catalog'."""
        self.open()
        self.click((By.LINK_TEXT, link_text))
