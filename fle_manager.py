import asyncio
import json

import aiohttp
import aiofile

from aiohttp import ClientSession


class DownloadUtils:
    async def __save_multimedia_data_to_file(self, url: str, session: ClientSession,
                                             path_with_name_and_extension: str) -> None:
        """ Скачивает данные чанками и сохраняет в файл, указанного формата """
        async with session.get(url) as response:
            async with aiofile.async_open(path_with_name_and_extension, 'xb+') as file:
                async for chunk in response.content.iter_chunked(1024):
                    await file.write(chunk)

    async def __save_multimedia_data_runner(self, files_links: dict | str, save_directory: str, extension: str,
                                            film_name: str) -> None:
        """ Создаёт задачи и ждёт их выполнения """
        if isinstance(files_links, str):
            urls = (files_links,)
            names = ('',)
        else:
            urls = files_links.keys()
            names = files_links.values()

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.__save_multimedia_data_to_file(url, session, fr'{save_directory}{film_name}_{name}.{extension}')
                for url in urls
                for name in names]
            await asyncio.gather(*tasks, return_exceptions=True)

    def save_multimedia_files(self, files_links: dict | str, save_directory: str, extension: str,
                              film_name: str) -> None:
        """ Запускает ранер """
        asyncio.run(self.__save_multimedia_data_runner(files_links, save_directory, extension, film_name))

    def save_info_to_json(self, data: dict, save_directory: str, name: str) -> None:
        """ Сохраняет данные в файл в формате JSON """
        with open(fr'{save_directory}{name}.json', 'a+') as file:
            json.dump(data, file, ensure_ascii=False)


class UploadUtils:
    async def __read_multimedia_data_from_local_storage(self, path_with_name_and_extension: str, key: str,
                                                        session: ClientSession, url: str, headers: dict) -> str:
        """ Считывает данные из файла и загружает, по указанному url """
        async with aiofile.async_open(path_with_name_and_extension, 'rb') as file:
            data = await file.read()
            async with session.post(url=url, data={key: data}, headers=headers) as response:
                result = await response.text()
                return result

    async def __upload_multimedia_data_runner(self, files: dict, url: str, headers: dict = None) -> list:
        """ Создаёт задачи и ждёт их выполнения """
        if headers is None:
            headers = {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.__read_multimedia_data_from_local_storage(file, key, session, url, headers)
                     for file in list(files.values())[0]
                     for key in files.keys()]
            result = await asyncio.gather(*tasks, return_exceptions=True)
            return result

    def upload_multimedia_files_to_storage(self, files: dict, url: str, headers: dict) -> list:
        """ Запускает ранер """
        result = asyncio.run(self.__upload_multimedia_data_runner(files, url, headers))
        return result
