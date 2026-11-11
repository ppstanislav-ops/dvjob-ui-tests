import os
import re

import allure
import dotenv
import pytest
from playwright.sync_api import expect

from pages.server_validation_page import ServerValidationAuthPage

dotenv.load_dotenv()

# Эпик/фича вынесены в env, чтобы не публиковать конкретный сайт в открытом репо.
EPIC = os.getenv("ALLURE_EPIC", "UI тестирование")
FEATURE = os.getenv("ALLURE_FEATURE", "Серверная валидация")


ROLE_CONFIG = {
    "candidate": {
        "story": "Валидация поля username при авторизации соискателя",
        "login_method": "login_candidate_and_capture_response",
        "success_url_pattern": re.compile(r"/my/resumes"),
        "default_email_attr": "DEFAULT_EMAIL",
    },
    "employer": {
        "story": "Валидация поля username при авторизации работодателя",
        "login_method": "login_employer_and_capture_response",
        "success_url_pattern": re.compile(r"/my/vacancies"),
        "default_email_attr": "DEFAULT_EMPLOYER_EMAIL",
    },
}


@pytest.mark.parametrize("role", ["candidate", "employer"])
@pytest.mark.parametrize(
    "bad_username, expected_status, expected_error_code",
    [
        # --- Некорректный ввод / несуществующий аккаунт → 404 account_not_found ---
        ("Tyyyuail.ru",               404, "account_not_found"),
        ("not_an_email",              404, "account_not_found"),
        ("user@",                     404, "account_not_found"),
        ("@example.com",              404, "account_not_found"),
        ("Εmail@test.com",            404, "account_not_found"),  # омоглифы (греческая Ε)
        ("' OR 1=1 --",               404, "account_not_found"),  # SQL-инъекция
        ("<script>alert(1)</script>", 404, "account_not_found"),  # XSS
        ("a" * 10_000,                404, "account_not_found"),  # очень длинная строка
        # --- Пустые / пробельные → 422 validation_error ---
        ("",                          422, "validation_error"),
        ("   ",                       422, "validation_error"),
    ],
    ids=[
        "несуществующий",
        "без_собаки",
        "без_домена",
        "без_локальной_части",
        "омоглифы",
        "sql_injection",
        "xss_payload",
        "превышение_длины",
        "пустой",
        "только_пробелы",
    ],
)
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.severity(allure.severity_level.CRITICAL)
def test_sign_in_server_validation(
    validation_page: ServerValidationAuthPage,
    role: str,
    bad_username: str,
    expected_status: int,
    expected_error_code: str,
):
    """Невалидный username не должен приводить к успешной авторизации.

    Параметризован по роли (соискатель/работодатель) и по типу невалидного
    username. Роль определяет сценарий логина, ожидаемый редирект и email
    по умолчанию для fallback-перехвата.
    """
    config = ROLE_CONFIG[role]

    # Динамические метки Allure — видны в отчёте по каждому кейсу.
    # bad_username в заголовок не выводим целиком (может содержать длинные
    # payload'ы) — для деталей используем label.
    allure.dynamic.story(config["story"])
    allure.dynamic.title(
        f"[{role}] Сервер отклоняет невалидный username "
        f"со статусом {expected_status} ({expected_error_code})"
    )
    allure.dynamic.label("role", role)
    allure.dynamic.label("bad_username", bad_username)
    allure.dynamic.label("expected_status", str(expected_status))
    allure.dynamic.label("expected_error_code", expected_error_code)

    with allure.step("Установка перехвата с подменой username"):
        validation_page.setup_username_interception(
            bad_username,
            original_email=getattr(validation_page, config["default_email_attr"]),
        )

    with allure.step("Выполнение авторизации и перехват ответа API"):
        response = getattr(validation_page, config["login_method"])()

    body = response.json()

    with allure.step("Проверка: токен не выдаётся ни при каких условиях"):
        assert body.get("success") is not True, (
            f"СЕРЬЁЗНО: сервер принял невалидный username как валидный! "
            f"status={response.status}, body={response.text()}"
        )
        data = body.get("data")
        assert not (isinstance(data, dict) and "token" in data), (
            f"СЕРЬЁЗНО: сервер выдал токен для невалидного username! "
            f"body={response.text()}"
        )

    with allure.step(f"Проверка: HTTP-статус = {expected_status}"):
        assert response.status == expected_status, (
            f"Ожидали статус {expected_status}, получили {response.status}: "
            f"{response.text()}"
        )

    with allure.step(f"Проверка: error_code = {expected_error_code}"):
        assert body.get("error_code") == expected_error_code, (
            f"Ожидали error_code={expected_error_code!r}, "
            f"получили {body.get('error_code')!r}: {response.text()}"
        )

    with allure.step("Проверка: фронт остаётся на странице логина"):
        expect(validation_page.page).not_to_have_url(
            config["success_url_pattern"], timeout=5_000
        )
        expect(validation_page.page).to_have_url(
            re.compile(r"/account/sign-in"), timeout=5_000
        )