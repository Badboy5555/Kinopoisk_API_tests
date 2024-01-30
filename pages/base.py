import requests
import json

from typing import BinaryIO

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

from locators.locators import BasePageLocators
from environments import StorageAPI


class BasePage:
    locators = BasePageLocators()

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)

    def go_to(self, locator: tuple, timeout=5) -> None:
        self.element_is_visible(locator, timeout).click()

    def element_is_visible(self, locator: tuple, timeout=5) -> WebElement:
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator: tuple, timeout=5) -> list[WebElement, ...]:
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def element_is_present(self, locator: tuple, timeout=5) -> WebElement:
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def elements_are_present(self, locator: tuple, timeout=5) -> list[WebElement, ...] | list:
        try:
            return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def find_elements(self, locator: tuple) -> list[WebElement, ...]:
        return self.driver.find_elements(locator)

    def element_is_clickable(self, locator: tuple, timeout=5) -> WebElement:
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def select_value_by_index(self, elem: WebElement, index: int) -> None:
        """ Выбирает элемент селектора по индексу """
        select = Select(elem)
        i = select.options[index].text
        select.select_by_value(i)

    def save_info_to_json(self, data: dict, save_directory: str, name: str) -> None:
        """ Сохраняет данне в файл в формате JSON """
        with open(fr'{save_directory}{name}.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False)

    def save_image_as_png(self, url, save_directory: str, name: str) -> None:
        """ Сохраняет данне в файл в формате PNG """
        image_data = requests.get(url).content
        with open(fr'{save_directory}{name}.png', 'wb') as file:
            file.write(image_data)

    def upload_info_to_storage(self, file: [str, BinaryIO], headers: dict = None) -> requests.Response:
        """ Загружает файл на хостинг https://api.imageban.ru/v1 """
        if headers is None:
            headers = {}
        CLIENT_ID = StorageAPI.API_CLIENT_ID_AUTHORIZATION_TOKEN
        url = StorageAPI.BASE_API_URL
        headers.update({'Authorization': f'TOKEN {CLIENT_ID}'})
        response = requests.post(url, files=file, headers=headers)
        return response.json()

    def download_video_file(self, url: str, save_directory: str, name: str) -> None:
        """ Скачивает видео по ссылке в файл в формате MP4"""
        response = requests.get(url, stream=True, allow_redirects=True)
        with open(fr'{save_directory}{name}.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=14):
                if chunk:
                    file.write(chunk)
