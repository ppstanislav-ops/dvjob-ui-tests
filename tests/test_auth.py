import os
import dotenv
import allure
from playwright.sync_api import expect
from pages.auth_page import AuthPage

dotenv.load_dotenv()

# Добавляем эпик
EPIC = "UI тестирование dvjob.kz"
# Метка фичи — общая для всех тестов модуля
FEATURE = "Авторизация"


# ========== Соискатель ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация соискателя")
@allure.title("Авторизация соискателя с валидными данными открывает страницу резюме")
@allure.severity(allure.severity_level.BLOCKER)
def test_auth_valid_candidate(auth: AuthPage):

    login = os.getenv("CandidateLogin")
    password = os.getenv("CandidatePassword")

    auth.login_as_candidate(login, password)
    expect(auth.page).to_have_url("https://dvjob.kz/ru/my/resumes", timeout=15_000)

@allure.epic(EPIC)
@allure.story("Авторизация соискателя")
@allure.title("Авторизация соискателя с невалидным паролем показывает ошибку «Аккаунт недействителен»")
@allure.severity(allure.severity_level.NORMAL)
def test_auth_not_valid_candidate(auth: AuthPage):
    auth.login_as_candidate("test25@mail.ru", "225445111")
    expect(auth.error_message).to_contain_text("Аккаунт не найден", timeout=15_000)


# ========== Работодатель ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация работодателя")
@allure.title("Авторизация работодателя с валидными данными открывает страницу вакансий")
@allure.severity(allure.severity_level.BLOCKER)
def test_auth_valid_employer(auth: AuthPage):
    login = os.getenv("EmployerLogin")
    password = os.getenv("EmployerPassword")

    auth.login_as_employer(login, password)
    expect(auth.page).to_have_url("https://dvjob.kz/ru/my/vacancies",timeout=15_000)

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Авторизация работодателя")
@allure.title("Авторизация работодателя с невалидным паролем показывает сообщение об ошибке")
@allure.severity(allure.severity_level.NORMAL)
def test_auth_not_valid_employer(auth: AuthPage):


    auth.login_as_employer("test@test.com", "1025889056")
    expect(auth.error_message).to_be_visible(timeout=15_000)




