import allure
from playwright.sync_api import expect

from pages.home_page import HomePage

# Добавляем эпик
EPIC = "UI тестирование dvjob.kz"
# Метка фичи — общая для всех тестов модуля
FEATURE = "Главная страница"

# ========== Заголовок и логотип ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Заголовок и логотип")
@allure.title("Заголовок страницы — «Международная платформа по поиску работы»")
@allure.severity(allure.severity_level.NORMAL)
def test_title(home: HomePage):
    expect(home.page).to_have_title("Международная платформа по поиску работы")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Заголовок и логотип")
@allure.title("Клик по логотипу открывает главную страницу /ru")
@allure.severity(allure.severity_level.NORMAL)
def test_logo(home: HomePage):
    home.click_logo()
    with allure.step("Проверка: после клика отображается главная страница"):
     expect(home.page).to_have_url("https://dvjob.kz/ru")


# ========== Навигационные элементы ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные элементы")
@allure.title("Клик «Dipcoin» открывает страницу дипкойна")
@allure.severity(allure.severity_level.NORMAL)
def test_dipcoin(home: HomePage):
    home.click_dipcoin()
    with allure.step("Проверка: после клика идет переход на страницу дипкойна"):
     expect(home.page).to_have_url("https://dvjob.kz/ru/dipcoin")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Языки")
@allure.title("Переключение языка на казахский открывает /kz")
@allure.severity(allure.severity_level.NORMAL)
def test_language_link_kz(home: HomePage):
    home.select_kz_language()
    with allure.step("Проверка: идет переход на страницу KZ"):
     expect(home.page).to_have_url("https://dvjob.kz/kz")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Языки")
@allure.title("Переключение языка на английский открывает /en")
@allure.severity(allure.severity_level.NORMAL)
def test_language_link_en(home: HomePage):
    home.select_en_language()
    with allure.step("Проверка: идет переход на страницу EN"):
     expect(home.page).to_have_url("https://dvjob.kz/en")


# ========== Поиск ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Найти работу» открывает страницу вакансий")
@allure.severity(allure.severity_level.BLOCKER)
def test_click_find_job(home: HomePage):
    home.click_find_job()
    with allure.step("Проверка: идет переход на страницу с вакансиями"):
     expect(home.page).to_have_url("https://dvjob.kz/ru/vacancies")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Найти сотрудника» открывает страницу резюме")
@allure.severity(allure.severity_level.BLOCKER)
def test_click_find_employ(home: HomePage):
    home.click_find_employee()
    with allure.step("Проверка: идет переход на страницу с резюме"):
     expect(home.page).to_have_url("https://dvjob.kz/ru/resumes")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Клик «Новое резюме» открывает страницу создания резюме /ru/resumes/new")
@allure.severity(allure.severity_level.NORMAL)
def test_click_new_resume(home: HomePage):
   home.click_new_resumes()
   with allure.step("Проверка: идет переход на страницу размещения нового резюме"):
    expect(home.page).to_have_url("https://dvjob.kz/ru/resumes/new")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Поиск вакансий по запросу «Менеджер» возвращает результаты")
@allure.severity(allure.severity_level.BLOCKER)
def test_search_vacancies(home: HomePage):
    query = "Менеджер"
    home.search_vacancies(query)
    with allure.step("Проверка: идет переход на страницу с вакансиями Менеджер"):
     expect(home.vacancy_results.first).to_be_visible(timeout=30_000)

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Поиск")
@allure.title("Поиск резюме по запросу «Менеджер» возвращает результаты")
@allure.severity(allure.severity_level.BLOCKER)
def test_search_resumes(home: HomePage):
    home.search_resumes("Менеджер")
    with allure.step("Проверка: идет переход на страницу с резюме Менеджер"):
     expect(home.resume_results.first).to_be_visible(timeout=30_000)


# ========== Визуальные элементы ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Визуальные элементы")
@allure.title("Изображения блока услуг отображаются на странице")
@allure.severity(allure.severity_level.MINOR)
def test_images_to_be_visible(home: HomePage):
    home.check_services_images()


# ========== Промо и виджеты ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Промо и виджеты")
@allure.title("Клик «Акции» открывает страницу с акциями")
@allure.severity(allure.severity_level.NORMAL)
def test_promotions(home: HomePage):
    home.click_promotions()
    with allure.step("Проверка: идет переход на страницу с акциями"):
     expect(home.page).to_have_url('https://dvjob.kz/ru/promotions', timeout=30_000)

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Промо и виджеты")
@allure.title("Чат поддержки открывается и отображается виджет")
@allure.severity(allure.severity_level.NORMAL)
def test_chat_widget(home: HomePage):
    home.open_chat_support()
    with allure.step("Проверка: отображается чат поддержки"):
     expect(home.chat_widget_container).to_be_visible(timeout=5000)
