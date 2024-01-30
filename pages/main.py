from pages.base import BasePage
from locators.locators import MailPageLocators


class MainPage(BasePage):

    locators = MailPageLocators()

    def simple_search(self, search_string: str) -> None:
        """ Выполняет поиск без параметров (не расширенный) с результатами на странице поиска  """
        self.element_is_visible(self.locators.SEARCH_FIELD).send_keys(search_string)
        self.element_is_visible(self.locators.SEARCH_BUTTON).click()
