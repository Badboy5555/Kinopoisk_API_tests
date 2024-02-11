from pages.base import BasePage
from services.fle_manager import DownloadUtils
from locators.locators import FilmPageLocators


class FilmPage(BasePage):
    locators = FilmPageLocators()
    downloader = DownloadUtils()

    def get_film_name(self) -> str:
        """ Возвращает название фильма """
        return self.element_is_visible(self.locators.FILM_NAME).text

    def get_film_rating(self) -> str:
        """ Возвращает рэйтинг фильма """
        return self.element_is_visible(self.locators.FILM_RATING).text

    def get_film_about_info(self) -> dict:
        """ Возвращает  информацию из блока "О фильме" в виде словаря """
        titles = self.elements_are_visible(self.locators.TABLE_TITLES)
        values = self.elements_are_visible(self.locators.TABLE_VALUES)
        return {title.text: value.text for title, value in zip(titles, values)}

    def save_film_poster(self, film_name: str) -> None:
        """ Сохраняет обложку фолиьма в  файл в формате PNG по пути film_data/main_image """
        poster_image_src = self.element_is_visible(self.locators.FILM_POSTER_IMAGE).get_attribute('src')
        self.downloader.save_images_as_png(poster_image_src, './film_data/main_image/', film_name)

    def save_film_info(self, name: str) -> None:
        """ Сохраняет информацию о фолиьме в  файл в формате JSON по пути film_data/info """
        film_info = self.get_film_about_info()
        self.downloader.save_info_to_json(film_info, './film_data/info/', f'{name}_info')

    def go_to_image_section_page(self) -> None:
        """ Переходит на страницу с изображениями """
        self.go_to(self.locators.IMAGES_SECTION_PAGE)

    def go_to_review_section_page(self) -> None:
        """ Переходит на страницу с рецензиями """
        self.go_to(self.locators.REVIEWS_SECTION_PAGE)

    def go_to_trailer_section_page(self) -> None:
        """ Переходит на страницу с рецензиями """
        self.go_to(self.locators.TRAILERS_SECTION_PAGE)
