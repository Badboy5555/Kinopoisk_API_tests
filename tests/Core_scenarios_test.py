import pytest

from pages.main import MainPage
from pages.search import SearchPage
from pages.film.film import FilmPage
from pages.film.images import ImagesPage
from pages.film.reviews import ReviewsPage
from pages.film.trailers import TrailersPage


class TestUUID:
    @pytest.mark.parametrize('film', ['Ирония судьбы, или С легким паром!'])
    def test_UUID(self, driver, get_build_url, film):
        self.main_page = MainPage(driver)
        # Перейти на сайт Кинопоиска
        self.main_page.open(get_build_url)

        # Найти в поиске фильм
        self.main_page.simple_search(film)

        self.search_page = SearchPage(driver)
        searched_film_year = self.search_page.get_searched_film_year()
        searched_film_rating = self.search_page.get_searched_film_rating()

        # Перейти в карточку найденного фильма
        self.search_page.go_to_searched_film_page()

        self.film_page = FilmPage(driver)

        # Сравнить
        film_about_info = self.film_page.get_film_about_info()
        film_name = self.film_page.get_film_name()
        film_rating = self.film_page.get_film_rating()
        film_year = film_about_info['Год производства']

        assert film in film_name, f'Названия фильма отличаются. Страница фильма:  {film}, страница поиска: {film_name}'
        assert film_rating == searched_film_rating, \
            f'Рейтинги отличаются. Страница фильма: {film_rating}, страница поиска: {searched_film_rating}'
        assert film_year == searched_film_year, \
            f'Года не отличаются. Страница фильма: {film_year}, страница поиска: {searched_film_year}'

        # Сохранить обложку в каталог film_data/main_image/
        self.film_page.save_film_poster(film)
        # Сохранить информацию о фильме из блока "О фильме" в JSON файле в каталоге film_data/info/
        self.film_page.save_film_info(film)

        # Перейти в раздел "Изображения"
        self.film_page.go_to_image_section_page()

        self.images_page = ImagesPage(driver)
        # Сохранить все имеющиеся изображения в каталог film_data/other_images/
        self.images_page.save_all_pictures()

        # Перейти в раздел "Рецензии"
        self.images_page.go_back_to_film_page()
        self.film_page.go_to_review_section_page()

        self.reviews_page = ReviewsPage(driver)
        # Сохранить все рецензии каждого типа в JSON-файл в каталоге film_data/info/
        self.reviews_page.save_reviews_to_json(film)

        # Все сохраненные изображения загрузить на любой хостинг изображений через API и ссылки
        # положить в JSON файле в каталоге film_data/images_links/
        links_list = self.images_page.upload_images_to_storage()
        self.images_page.save_images_links(film, links_list)
        self.images_page.go_back_to_film_page()
        self.film_page.go_to_trailer_section_page()

        self.trailer_page = TrailersPage(driver)

        # Сохранить все трейлеры к фильму в каталог film_data/videos/
        # self.trailer_page.download_all_trailer(film)
