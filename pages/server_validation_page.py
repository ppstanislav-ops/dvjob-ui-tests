import json
import os
import re
from typing import Optional

import allure
import dotenv
from playwright.sync_api import Route, Response, expect

from pages.auth_page import AuthPage

dotenv.load_dotenv()


class ServerValidationAuthPage(AuthPage):
    """Page Object для проверки серверной валидации при авторизации.

    Расширяет AuthPage, добавляя:
      - перехват запроса на /v1/accounts/sign-in с подменой поля username;
      - ожидание и возврат ответа API после отправки формы;
      - аттач отправленного тела и ответа в Allure-отчёт.

    Поддерживает два сценария:
      - соискатель: login_candidate_and_capture_response() / /my/resumes;
      - работодатель: login_employer_and_capture_response() / /my/vacancies.
    """

    SIGN_IN_API_PATTERN = re.compile(r"/v1/accounts/sign-in")

    # Учётные данные по умолчанию для каждой роли берутся из .env
    DEFAULT_EMAIL = os.getenv("CandidateLogin")
    DEFAULT_PASSWORD = os.getenv("CandidatePassword")
    DEFAULT_EMPLOYER_EMAIL = os.getenv("EmployerLogin")
    DEFAULT_EMPLOYER_PASSWORD = os.getenv("EmployerPassword")

    def __init__(self, page):
        super().__init__(page)
        self._last_intercepted_data: Optional[str] = None

    # ------------------------------------------------------------------
    # Перехват запроса
    # ------------------------------------------------------------------

    def setup_username_interception(
        self,
        bad_username: str,
        original_email: Optional[str] = None,
    ) -> None:
        """Регистрирует route handler, подменяющий username в теле запроса.

        Фронт всегда отправляет валидный email через форму; перехват подменяет
        поле username в JSON-теле на bad_username. Так мы проверяем именно
        серверную валидацию, а не фронтовую.

        Параметр original_email нужен только для fallback-ветки (если тело
        запроса оказалось не JSON): в этом случае делается строковая замена
        исходного email на bad_username. По умолчанию берётся email соискателя;
        для сценария работодателя передаётся DEFAULT_EMPLOYER_EMAIL.
        """
        original_email = original_email or self.DEFAULT_EMAIL

        def change_request(route: Route):
            data = route.request.post_data
            if data:
                try:
                    payload = json.loads(data)
                    if "username" in payload:
                        payload["username"] = bad_username
                    data = json.dumps(payload)
                except json.JSONDecodeError:
                    data = data.replace(original_email, bad_username)
            self._last_intercepted_data = data
            print(f"[INTERCEPT] URL={route.request.url} sent_data={data!r}")
            route.continue_(post_data=data)

        self.page.route(self.SIGN_IN_API_PATTERN, change_request)

    # ------------------------------------------------------------------
    # Авторизация с перехватом ответа
    # ------------------------------------------------------------------

    def login_candidate_and_capture_response(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Response:
        """Полный сценарий входа соискателя с ожиданием ответа API.

        Параметры email/password по умолчанию берутся из DEFAULT_*
        (значения приходят из .env — см. DEFAULT_EMAIL / DEFAULT_PASSWORD).
        Возвращает Response от /v1/accounts/sign-in.
        """
        email = email or self.DEFAULT_EMAIL
        password = password or self.DEFAULT_PASSWORD

        # 1. Ждём, что Vue примонтирован
        self.page.wait_for_function(
            "() => !!document.getElementById('__nuxt')?.__vue_app__",
            timeout=15_000,
        )

        # 2. Выбор роли с ретраями (до гидратации Vue клик может "глотаться")
        with allure.step("Выбор роли «Я ищу работу»"):
            self._select_candidate_role_with_retries()

        # 3. Переход к форме авторизации
        with allure.step("Открытие формы авторизации с паролем"):
            expect(self.login_button).to_be_enabled(timeout=5_000)
            self.login_button.click()
            self.login_with_password_button.click()

        # 4. Заполнение формы
        with allure.step(f"Заполнение формы: email={email!r}, password=***"):
            self.email_input.click()
            self.email_input.fill(email)
            self.password_input.click()
            self.password_input.fill(password)

        # 5. Отправка + перехват ответа
        with allure.step("Отправка формы и перехват ответа API"):
            expect(self.submit_button).to_be_enabled(timeout=5_000)
            with self.page.expect_response(
                self.SIGN_IN_API_PATTERN, timeout=10_000
            ) as resp_info:
                self.submit_button.click()
            response = resp_info.value

        # 6. Аттач в Allure
        self._attach_request_response_to_allure(response)

        print(f"[RESPONSE] status={response.status} body={response.text()!r}")
        return response

    def login_employer_and_capture_response(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Response:
        """Полный сценарий входа работодателя с ожиданием ответа API.

        Параметры email/password по умолчанию берутся из DEFAULT_EMPLOYER_*
        (значения приходят из .env — см. DEFAULT_EMPLOYER_EMAIL /
        DEFAULT_EMPLOYER_PASSWORD). Возвращает Response от /v1/accounts/sign-in.

        Отличия от кандидатского сценария:
          - выбирается роль «Я ищу сотрудников»;
          - после нажатия «Войти» дополнительно переключаемся на вкладку
            «Почта» (email_tab_button) перед переходом к форме с паролем.
        """
        email = email or self.DEFAULT_EMPLOYER_EMAIL
        password = password or self.DEFAULT_EMPLOYER_PASSWORD

        # 1. Ждём, что Vue примонтирован
        self.page.wait_for_function(
            "() => !!document.getElementById('__nuxt')?.__vue_app__",
            timeout=15_000,
        )

        # 2. Выбор роли работодателя с ретраями
        with allure.step("Выбор роли «Я ищу сотрудников»"):
            self._select_employer_role_with_retries()

        # 3. Переход к форме авторизации (вкладка «Почта» → «Войти с паролем»)
        with allure.step("Открытие формы авторизации с паролем"):
            expect(self.login_button).to_be_enabled(timeout=5_000)
            self.login_button.click()
            # Работодатель по умолчанию попадает на вкладку телефона —
            # переключаемся на email, чтобы поле username было email-адресом.
            expect(self.email_tab_button).to_be_visible(timeout=5_000)
            self.email_tab_button.click()
            self.login_with_password_button.click()

        # 4. Заполнение формы
        with allure.step(f"Заполнение формы: email={email!r}, password=***"):
            self.email_input.click()
            self.email_input.fill(email)
            self.password_input.click()
            self.password_input.fill(password)

        # 5. Отправка + перехват ответа
        with allure.step("Отправка формы и перехват ответа API"):
            expect(self.submit_button).to_be_enabled(timeout=5_000)
            with self.page.expect_response(
                self.SIGN_IN_API_PATTERN, timeout=10_000
            ) as resp_info:
                self.submit_button.click()
            response = resp_info.value

        # 6. Аттач в Allure
        self._attach_request_response_to_allure(response)

        print(f"[RESPONSE] status={response.status} body={response.text()!r}")
        return response

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------
    @allure.step("Выбор роли «Я ищу работу»")
    def _select_candidate_role_with_retries(self) -> None:
        """Клик по роли соискателя с ретраями до гидратации Vue.

        Аналогично _select_role из родителя, но с явными ретраями
        вместо фиксированного ожидания — устойчивее к плавающим таймингам.
        """
        role_btn = self.page.get_by_role(
            "button", name=re.compile("я ищу работу", re.I)
        )
        active = self.page.locator(".sign-in-role__option--active")

        for _ in range(5):
            role_btn.click()
            try:
                active.wait_for(state="visible", timeout=1_500)
                return
            except Exception:
                self.page.wait_for_timeout(500)
        raise AssertionError(
            "Роль не применилась после 5 кликов — вероятно, клик не обрабатывается"
        )

    @allure.step("Выбор роли «Я ищу сотрудников»")
    def _select_employer_role_with_retries(self) -> None:
        """Клик по роли работодателя с ретраями до гидратации Vue.

        Аналогично _select_candidate_role_with_retries, но для карточки
        «Я ищу сотрудников».
        """
        role_btn = self.page.get_by_role(
            "button", name=re.compile("я ищу сотрудников", re.I)
        )
        active = self.page.locator(".sign-in-role__option--active")

        for _ in range(5):
            role_btn.click()
            try:
                active.wait_for(state="visible", timeout=1_500)
                return
            except Exception:
                self.page.wait_for_timeout(500)
        raise AssertionError(
            "Роль не применилась после 5 кликов — вероятно, клик не обрабатывается"
        )

    @allure.step("Прикрепление данных запроса и ответа API в Allure")
    def _attach_request_response_to_allure(self, response: Response) -> None:
        """Прикладывает к Allure-отчёту отправленное тело и полученный ответ."""
        # Отправленное тело (после подмены)
        if self._last_intercepted_data:
            try:
                parsed = json.loads(self._last_intercepted_data)
                allure.attach(
                    json.dumps(parsed, ensure_ascii=False, indent=2),
                    name="Отправленное тело запроса (после подмены)",
                    attachment_type=allure.attachment_type.JSON,
                )
            except json.JSONDecodeError:
                allure.attach(
                    self._last_intercepted_data,
                    name="Отправленное тело запроса (после подмены)",
                    attachment_type=allure.attachment_type.TEXT,
                )

        # Ответ API
        allure.attach(
            f"URL: {response.url}\n"
            f"Status: {response.status}\n"
            f"Body: {response.text()}",
            name="Ответ API авторизации",
            attachment_type=allure.attachment_type.TEXT,
        )
