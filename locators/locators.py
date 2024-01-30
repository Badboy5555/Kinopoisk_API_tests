from selenium.webdriver.common.by import By


class BasePageLocators:
    TAG_BODY = (By.TAG_NAME, 'html')


class MailPageLocators(BasePageLocators):
    SEARCH_FIELD = (By.CSS_SELECTOR, '[name=kp_query]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '[aria-label="Найти"][type="submit"]')


class SearchPageLocators(BasePageLocators):
    # Поисковой блок "Скорее всего, вы ищете"
    MOST_WANTED_FILM_LINK = (By.CSS_SELECTOR, '.most_wanted .name>a')
    MOST_WANTED_FILM_YEAR = (By.CSS_SELECTOR, '.most_wanted .name>.year')
    MOST_WANTED_FILM_RATING = (By.CSS_SELECTOR, '.most_wanted .rating')


class FilmPageLocators(BasePageLocators):
    FILM_NAME = (By.CSS_SELECTOR, '[itemprop="name"]')
    FILM_RATING = (By.XPATH, '//span[contains(@class,"film-rating-value")]/span[@aria-hidden="true"]')

    # Таблица с информацией о флиьме
    TABLE_TITLES = (By.XPATH, '//div[@data-test-id="encyclopedic-table"]//div[contains(@class,"styles_title")]')
    TABLE_VALUES = (By.XPATH, '//div[@data-test-id="encyclopedic-table"]//div[contains(@class,"styles_title")]/'
                              'following-sibling::div')

    FILM_POSTER_IMAGE = (By.CSS_SELECTOR, '.film-poster')

    IMAGES_SECTION_PAGE = (By.XPATH, '//ul//a[contains(@class, "styles_itemDefault") and text()="Изображения"]')
    REVIEWS_SECTION_PAGE = (By.XPATH, '//ul//a[contains(@class, "styles_itemDefault") and text()="Рецензии"]')
    TRAILERS_SECTION_PAGE = (By.XPATH, '//ul//a[contains(@class, "styles_itemDefault") and text()="Трейлеры"]')


class ImagesPageLocators(BasePageLocators):
    IMAGES_TYPES = (By.XPATH, '//ul[contains(@class, "styles_imagesTypes")]//a')
    IMAGES = (By.XPATH, '//div[contains(@class, "styles_gallery")]/div//a[contains(@class, "styles_download")]')
    FIRST_IMAGE = (By.XPATH, '//div[contains(@class, "styles_gallery")]/div[1]')

    BACK_TO_FILM_PAGE = (By.XPATH, '//a[contains(@class, "styles_backLink")]')


class ReviewsPageLocators(BasePageLocators):
    SUMMARY_ALL = (By.CSS_SELECTOR, '.resp_type>.all>b')
    SUMMARY_POSITIVE = (By.CSS_SELECTOR, '.resp_type>.pos>b')
    SUMMARY_NEGATIVE = (By.CSS_SELECTOR, '.resp_type>.neg>b')
    SUMMARY_NEUTRAL = (By.CSS_SELECTOR, '.resp_type>.neut>b')

    REVIEW_POSITIVE = (By.CSS_SELECTOR, '.response.good')
    REVIEW_NEGATIVE = (By.CSS_SELECTOR, '.response.bad')
    REVIEW_NEUTRAL = (By.CSS_SELECTOR, '.response.neutral')
    REVIEW_TEXT = (By.TAG_NAME, 'table')

    PAGINATOR_NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, '.list>.arr>a')
    COUNT_PER_PAGE_SELECTOR_TOP = (By.CSS_SELECTOR, '.navigator_per_page')


class TrailersPageLocators(BasePageLocators):
    TRAILER_FRAME = (By.CSS_SELECTOR, '.movie-trailer-embed')
    TRAILER_LINK = (By.CSS_SELECTOR, '.discovery-trailers-embed-iframe')
