from playwright.sync_api import Locator
from pages.base_page import BasePage
import allure


class AuthPage(BasePage):
    """Page Object для страницы авторизации."""

    # Locators

    @property
    def candidate_card(self) -> Locator:
        return self.page.locator(".sign-in-role__option").first

    @property
    def employer_card(self) -> Locator:
        return self.page.locator(".sign-in-role__option").filter(
            has_text="Я ищу сотрудников"
        )

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Войти", exact=True)

    @property
    def email_tab_button(self) -> Locator:
        return self.page.get_by_role("button", name="Почта")

    @property
    def login_with_password_button(self) -> Locator:
        return self.page.get_by_role("button", name="Войти с паролем", exact=True)

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="Введите email")

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="Введите пароль")

    @property
    def submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Войти", exact=True)

    @property
    def error_message(self) -> Locator:
        return self.page.locator(".invalid-feedback")


    # Actions

    @allure.step("Выбор роли по карточке")
    def _select_role(self, card: Locator) -> None:
        """Клик по карточке роли с ожиданием активации."""
        card.wait_for(state="visible")
        card.locator(".sign-in-role__option-title").click()
        self.page.wait_for_timeout(1500)

    # Если роль не активировалась — кликаем по самой карточке
        if "sign-in-role__option--active" not in (card.get_attribute("class") or ""):
            card.click(force=True)
            self.page.wait_for_timeout(1500)

    @allure.step("Заполнение формы авторизации: email={email}")
    def _fill_credentials(self, email: str, password: str) -> None:
        """Заполняет форму авторизации."""
        self.email_input.click()
        self.email_input.fill(email)
        self.password_input.click()
        self.password_input.fill(password)
        self.submit_button.click()

    @allure.step("Выбор роли: Соискатель")
    def select_candidate_role(self) -> None:
        """Выбирает роль соискателя."""
        self._select_role(self.candidate_card)

    @allure.step("Выбор роли: Работодатель")
    def select_employer_role(self) -> None:
        """Выбирает роль работодателя."""
        self._select_role(self.employer_card)

    @allure.step("Авторизация соискателя")
    def login_as_candidate(self, email: str, password: str) -> None:
        """Полный сценарий входа соискателя."""
        self.select_candidate_role()
        self.login_button.click()
        self.login_with_password_button.click()
        self._fill_credentials(email, password)

    @allure.step("Авторизация работодателя")
    def login_as_employer(self, email: str, password: str) -> None:
        """Полный сценарий входа работодателя."""
        self.select_employer_role()
        self.login_button.click()
        self.email_tab_button.click()
        self.login_with_password_button.click()
        self._fill_credentials(email, password)