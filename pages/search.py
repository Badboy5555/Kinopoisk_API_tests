from pages.base import BasePage
from locators.locators import SearchPageLocators


class SearchPage(BasePage):
    locators = SearchPageLocators()

    def get_searched_film_link(self) -> str:
        """ Возвращает ссылку на страницу фильма """
        return self.element_is_visible(self.locators.MOST_WANTED_FILM_LINK).get_attribute('href')

    def get_searched_film_year(self) -> str:
        """ Возвращает год выхода фильма """
        return self.element_is_visible(self.locators.MOST_WANTED_FILM_YEAR).text

    def get_searched_film_rating(self):
        """ Возвращает рэйтинг фильма """
        return self.element_is_visible(self.locators.MOST_WANTED_FILM_RATING).text

    def go_to_searched_film_page(self) -> None:
        """ Переходит на страницу фильма из блока "Скорее всего, вы ищете" """
        self.go_to(self.locators.MOST_WANTED_FILM_LINK)
