import json
import os
import platform
import sys

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.footer_page import FooterPage
from pages.auth_page import AuthPage
from pages.server_validation_page import ServerValidationAuthPage


BASE_URL = "https://dvjob.kz"

# Файл, в котором хранится счётчик запусков (нужен для buildOrder в истории)
BUILD_ORDER_FILE = ".build_order"


@pytest.fixture(autouse=True)
def setup_page(page: Page):
    """Общие настройки для всех тестов (без навигации)."""
    page.set_default_navigation_timeout(60_000)
    yield page


@pytest.fixture
def home(page: Page) -> HomePage:
    page.goto(f"{BASE_URL}/ru", wait_until="domcontentloaded")
    return HomePage(page)


@pytest.fixture
def footer(page: Page) -> FooterPage:
    page.goto(f"{BASE_URL}/ru", wait_until="domcontentloaded")
    return FooterPage(page)


@pytest.fixture
def auth(page: Page) -> AuthPage:
    page.goto(f"{BASE_URL}/ru/account/sign-in", wait_until="domcontentloaded")
    return AuthPage(page)

@pytest.fixture
def validation_page(page: Page) -> ServerValidationAuthPage:
        """Page Object для проверки серверной валидации при авторизации.

        Навигация на страницу логина выполняется здесь (до установки route),
        а сам route handler регистрируется в каждом тесте через
        setup_username_interception(bad_username), т.к. подменяемое значение
        специфично для каждого кейса.
        """
        vp = ServerValidationAuthPage(page)
        vp.page.goto(f"{BASE_URL}/ru/account/sign-in", wait_until="load")
        return vp

# ----- Заполнение Environment / Executors / Categories ----------------

def _next_build_order() -> int:
    """Сквозной номер запуска, чтобы во вкладке Trends были разные билды."""
    order = 0
    if os.path.exists(BUILD_ORDER_FILE):
        try:
            order = int(open(BUILD_ORDER_FILE, encoding="utf-8").read().strip())
        except ValueError:
            order = 0
    order += 1
    with open(BUILD_ORDER_FILE, "w", encoding="utf-8") as f:
        f.write(str(order))
    return order


def pytest_sessionfinish(session, exitstatus):
    """Пишет environment.properties, executor.json и categories.json
    в директорию allure-results после завершения прогона.

    Работает только если pytest запущен с --alluredir=<папка>.
    """
    allure_dir = getattr(session.config.option, "allure_report_dir", None)
    if not allure_dir:
        return

    # 1. Environment — виджет «Environment» на главной странице отчёта
    environment = {
        "Base URL": BASE_URL,
        "Browser": "Chromium (Playwright)",
        "Stand": "production",
        "Python": sys.version.split()[0],
        "OS": platform.platform(),
    }
    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding="utf-8") as f:
        for key, value in environment.items():
            f.write(f"{key}={value}\n")

    # 2. Executors — виджет «Executors» (кто и в каком билде запускал тесты)
    executor = {
        "name": "Local run",
        "type": "local",
        "buildName": "dvjob-ui-tests",
        "buildOrder": _next_build_order(),
    }
    with open(os.path.join(allure_dir, "executor.json"), "w", encoding="utf-8") as f:
        json.dump(executor, f, ensure_ascii=False, indent=2)

    # 3. Categories — свои категории вместо дефолтных «Product/Test defects».
    #    Наполняются автоматически, когда появляются упавшие/сломанные тесты.
    categories = [
        {"name": "Баги продукта", "matchedStatuses": ["failed"]},
        {"name": "Проблемы теста или окружения", "matchedStatuses": ["broken"]},
        {"name": "Известные проблемы (skipped)", "matchedStatuses": ["skipped"]},
    ]
    with open(os.path.join(allure_dir, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)


# ----- Allure reporting ----------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняем отчёт теста на узле, чтобы к нему можно было обратиться в фикстурах."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    """При падении теста прикладываем к Allure-отчёту скриншот, HTML и URL страницы."""
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name="Скриншот на месте падения",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                page.content(),
                name="HTML страницы",
                attachment_type=allure.attachment_type.HTML,
            )
            allure.attach(page.url, name="URL страницы")
        except Exception:
            # браузер мог быть уже закрыт — не роняем формирование отчёта
            pass








