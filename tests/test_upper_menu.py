import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

# Добавляем эпик
EPIC = "UI тестирование dvjob.kz"
# Метка фичи — общая для всех тестов модуля
FEATURE = "Верхнее меню"


# ========== Меню «Соискателю» ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Каталог вакансий» открывает страницу /ru/vacancies")
@allure.severity(allure.severity_level.CRITICAL)
def test_candidates_menu_vacancies(home: HomePage):
    home.click_vacancies_catalog()
    expect(home.page).to_have_url("https://dvjob.kz/ru/vacancies")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Советы по прохождению интервью» открывает страницу с правилами интервью")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_sovety(home: HomePage):
    home.click_interview_tips()
    expect(
        home.page.get_by_role("heading", name="правил прохождения интервью")
    ).to_be_visible()

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Заключение договора» открывает форму с заголовком «Заполните данные для заключения договора»")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_dogovor(home: HomePage):
    home.click_contract()
    expect(
        home.page.get_by_role("heading", name="Заполните данные для заключения договора")
    ).to_be_visible()

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Консультация юриста» перенаправляет на страницу входа /ru/account/sign-in")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_cons_lawyer(home: HomePage):
    home.click_lawyer_consult()
    expect(home.page).to_have_url("https://dvjob.kz/ru/account/sign-in")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Соискателю»")
@allure.title("Клик «Консультация бухгалтера» перенаправляет на страницу входа /ru/account/sign-in")
@allure.severity(allure.severity_level.NORMAL)
def test_candidates_menu_cons_buh(home: HomePage):
    home.click_accountant_consult()
    expect(home.page).to_have_url("https://dvjob.kz/ru/account/sign-in")


# ========== Меню «Работодателю» ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Меню «Работодателю»")
@allure.title("Клик «Каталог резюме» открывает страницу /ru/resumes")
@allure.severity(allure.severity_level.CRITICAL)
def test_employ_menu_resumes(home: HomePage):
    home.click_resumes_catalog()
    expect(home.page).to_have_url("https://dvjob.kz/ru/resumes")
