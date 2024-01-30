import time
import os
from pages.base import BasePage
from locators.locators import ImagesPageLocators


class ImagesPage(BasePage):
    locators = ImagesPageLocators()

    def save_all_pictures(self) -> None:
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

            for image_type in image_types_objects:
                for i, obj in enumerate(image_types_objects[image_type]):
                    image_link = obj.get_attribute('href')
                    self.save_image_as_png(image_link, './film_data/other_images/', f'{image_type}_image_{i}')

    def go_back_to_film_page(self) -> None:
        """ Переходит назад на страницу фильма """
        self.go_to(self.locators.BACK_TO_FILM_PAGE)

    def upload_images_to_storage(self) -> dict:
        images_links_list = {'images_links': []}
        path = r'./film_data/other_images/'
        images_list = os.listdir(path)

        for image in images_list:
            file = {'image': open(path + image, 'rb')}
            result = self.upload_info_to_storage(file)

            images_links_list['images_links'].append(
                {'image_name': result['data']['img_name'],
                 'image_link': result['data']['link']})
        return images_links_list

    def save_images_links(self, name: str, images_links_list: dict) -> None:
        """ Сохраняет ссыдки на изображения в  файл в формате JSON по пути film_data/images_links """
        self.save_info_to_json(images_links_list, './film_data/images_links/', f'{name}_links')
