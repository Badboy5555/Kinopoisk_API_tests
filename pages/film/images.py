import json
import time
import os

from pages.base import BasePage
from services.fle_manager import DownloadUtils, UploadUtils
from locators.locators import ImagesPageLocators
from environments import StorageAPI


class ImagesPage(BasePage):
    path = r'./film_data/other_images/'
    locators = ImagesPageLocators()
    downloader = DownloadUtils()
    uploader = UploadUtils()
    storage = StorageAPI()

    def save_all_images(self, film_name: str) -> None:
        """ Сохраняет все изображения в film_data/other_images/ """
        image_types = self.elements_are_visible(self.locators.IMAGES_TYPES)

        for _type in image_types:
            image_types_objects = {}
            concurrent_type = _type.get_attribute('href').split('/')[-2]
            _type.click()
            images = self.elements_are_present(self.locators.IMAGES)
            image_types_objects[concurrent_type] = images

            timer, switch_to_next = 2, False
            while timer > 0 and not images:
                if timer == 0:
                    timer = 2
                    _next = True
                    break
                time.sleep(0.5)
                images = self.elements_are_present(self.locators.IMAGES)
                timer -= 0.5

            if switch_to_next:
                break

            image_links = {}
            for image_type in image_types_objects:
                for i, obj in enumerate(image_types_objects[image_type]):
                    image_links[obj.get_attribute('href')] = f'{image_type}_image_{i}'

            self.downloader.save_multimedia_files(image_links, './film_data/other_images/', 'png', film_name)

    def go_back_to_film_page(self) -> None:
        """ Переходит назад на страницу фильма """
        self.go_to(self.locators.BACK_TO_FILM_PAGE)

    def upload_images_to_storage(self) -> dict:
        """" Загружает картинки на хостинг и возвращает ссылки """
        images_links = {'images_links': []}
        images = {'image': []}

        for file_name in os.listdir(self.path):
            images['image'].append(self.path + file_name)

        client_id = self.storage.API_CLIENT_ID_AUTHORIZATION_TOKEN
        url = self.storage.BASE_API_URL
        headers = {'Authorization': f'TOKEN {client_id}'}

        images_descriptions = self.uploader.upload_multimedia_files_to_storage(images, url, headers=headers)

        for description in images_descriptions:
            description = json.loads(description)
            images_links['images_links'].append(
                {'image_name': description['data']['img_name'],
                 'image_link': description['data']['link']})
        return images_links

    def save_images_links(self, name: str, images_links: dict) -> None:
        """ Сохраняет ссыдки на изображения в  файл в формате JSON по пути ./film_data/images_links/ """
        self.downloader.save_info_to_json(images_links, './film_data/images_links/', f'{name}_links')
