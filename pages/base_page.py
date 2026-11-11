import allure
from playwright.sync_api import Page

class BasePage:

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Ожидание загрузки страницы (DOMContentLoaded)")
    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")