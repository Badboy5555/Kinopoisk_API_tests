import os


class StorageAPI:
    BASE_API_URL = 'https://api.imageban.ru/v1'
    API_CLIENT_ID_AUTHORIZATION_TOKEN = os.getenv('STORAGE_CLIENT_ID')
    #API_CLIENT_ID_AUTHORIZATION_TOKEN = 'NSG4U9gDwQQF3JZcqTTe'
