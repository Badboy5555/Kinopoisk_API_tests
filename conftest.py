import pytest

from selenium.webdriver import Chrome


def pytest_addoption(parser):
    """ Добавляет необходимые опции командной строки """
    parser.addoption('--browser_name', action='store', default='Chrome', help='Выбор браузера: Chrome')
    parser.addoption('--build_url', action='store', help='url билда для тестирования')


@pytest.fixture(scope='function')
def get_build_url(request) -> str:
    """ Получить url проекта """
    return request.config.getoption('--build_url')


@pytest.fixture(scope='class')
def driver(request):
    """ Запускает нужный драйвер """
    browsers = {'Chrome': Chrome}
    browser_name = request.config.getoption('--browser_name')
    driver = browsers.get(browser_name)()
    driver.maximize_window()
    yield driver

    driver.quit()
