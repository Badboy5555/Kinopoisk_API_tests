import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from pages.base import BasePage
from locators.locators import TrailersPageLocators
from services.fle_manager import DownloadUtils


class TrailersPage(BasePage):
    locators = TrailersPageLocators()
    downloader = DownloadUtils()

    def trailer_click(self, elem: WebElement) -> None:
        elem.click()

    def download_all_trailers(self, name) -> None:
        """ Скачивает все трейлеры к фильму в каталог film_data/videos/ """

        trailers_list = self.elements_are_visible(self.locators.TRAILER_FRAME)
        trailers_links = {}

        for i, trailer in enumerate(trailers_list):
            self.trailer_click(trailer)
            timer = 5
            while timer != 0:
                try:
                    trailer_link = trailer.find_element(*self.locators.TRAILER_LINK).get_attribute('src')
                    break
                except NoSuchElementException:
                    time.sleep(0.5)
                    timer -= 0.5
            trailer_link = trailer_link.replace('noAd=0', 'noAd=1')
            trailers_links[trailer_link] = f'{name}_trailer_{i}'

        self.downloader.save_multimedia_files(trailers_links, './film_data/videos/', 'mp4',  name)
