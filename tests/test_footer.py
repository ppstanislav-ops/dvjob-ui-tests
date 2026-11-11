import re
import allure
import pytest
from playwright.sync_api import expect
from pages.footer_page import FooterPage


# Добавляем эпик
EPIC = "UI тестирование dvjob.kz"
# Метка фичи — общая для всех тестов модуля
FEATURE = "Футер"


# ========== Видимость ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Видимость")
@allure.title("Футер отображается на странице")
@allure.severity(allure.severity_level.CRITICAL)
def test_footer_visible(footer: FooterPage):
    expect(footer.footer).to_be_visible()

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Видимость")
@allure.title("В футере отображается текст с адресом компании")
@allure.severity(allure.severity_level.MINOR)
def test_footer_info(footer: FooterPage):
    expect(footer.address_text).to_be_visible()


# ========== Навигационные ссылки ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «О компании» открывает страницу О компании")
@allure.severity(allure.severity_level.CRITICAL)
def test_about(footer: FooterPage):
    footer.click_about()
    with allure.step("Проверка: идет переход на страницу «О компании»"):
     expect(footer.page).to_have_url("https://dvjob.kz/ru/about")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Соглашение об оказании услуг» открывает эту страницу")
@allure.severity(allure.severity_level.NORMAL)
def test_terms(footer: FooterPage):
    footer.click_terms()
    with allure.step("Проверка: идет переход на страницу «Соглашение об оказании услуг»"):
     expect(footer.page).to_have_url("https://dvjob.kz/ru/terms")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Политика конфиденциальности» открывает эту страницу")
@allure.severity(allure.severity_level.NORMAL)
def test_privacy(footer: FooterPage):
    footer.click_privacy()
    with allure.step("Проверка: идет переход на страницу «Политика конфиденциальности»"):
     expect(footer.page).to_have_url("https://dvjob.kz/ru/privacy")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Условия возврата» открывает страницу где описаны условия возврата")
@allure.severity(allure.severity_level.NORMAL)
def test_refund(footer: FooterPage):
    footer.click_refund()
    with allure.step("Проверка: идет переход на страницу «Условия возврата»"):
     expect(footer.page).to_have_url("https://dvjob.kz/ru/refund")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Навигационные ссылки")
@allure.title("Клик «Контакты» открывает страницу Контакты")
@allure.severity(allure.severity_level.NORMAL)
def test_contacts(footer: FooterPage):
    footer.click_contacts()
    with allure.step("Проверка: идет переход на страницу «Контакты»"):
     expect(footer.page).to_have_url("https://dvjob.kz/ru/contacts")


# ========== Контакты ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Контакты")
@allure.title("Телефон в футере: видимый номер и корректная ссылка на номер телефона")
@allure.severity(allure.severity_level.CRITICAL)
def test_footer_phone(footer: FooterPage):
    with allure.step("Телефон отображается"):
        expect(footer.phone_link).to_be_visible()

    with allure.step("Отображаемый номер содержит +7(777) 8155015"):
        expect(footer.phone_link).to_contain_text("+7(777) 8155015")

    with allure.step("Ссылка содержит только цифры номера телефона 77778155015"):
        href = footer.phone_link.get_attribute("href")
        allure.attach(href or "<href отсутствует>", name="phone href")
        digits = re.sub(r"\D", "", href or "")
        assert digits == "77778155015", f"Unexpected phone href: {href!r}"

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Контакты")
@allure.title("E-mail в футере: текст ссылки и mailto:-href")
@allure.severity(allure.severity_level.NORMAL)
def test_footer_email(footer: FooterPage):
    with allure.step("E-mail отображается"):
        expect(footer.email_link).to_be_visible()

    with allure.step("Текст ссылки — info@dvjob.kz"):
        expect(footer.email_link).to_contain_text("info@dvjob.kz")

    with allure.step("ссылка — mailto:info@dvjob.kz"):
        expect(footer.email_link).to_have_attribute("href", "mailto:info@dvjob.kz")


# ========== Текстовый контент ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("В футере указан полный адрес: г.Алматы, пр. Достык 202, оф. 202")
@allure.severity(allure.severity_level.MINOR)
def test_footer_address_full(footer: FooterPage):
    expect(footer.footer).to_contain_text("г.Алматы, пр. Достык 202, оф. 202")

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("Отображается блок копирайта")
@allure.severity(allure.severity_level.TRIVIAL)
def test_footer_copyright(footer: FooterPage):
    expect(footer.copyright_text).to_be_visible()

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Текстовый контент")
@allure.title("Отображается юридическое уведомление")
@allure.severity(allure.severity_level.TRIVIAL)
def test_footer_legal_notice(footer: FooterPage):
    expect(footer.legal_notice_text).to_be_visible()


# ========== Соцсети ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Соцсети")
@allure.title("Отображается иконка соцсети: {href}")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("href", [
    "https://t.me/allsetpro",
    "https://wa.me/77778155015",
    "https://www.instagram.com/dvjob.kz",
])
def test_footer_social_links(footer: FooterPage, href: str):
    expect(footer.get_social_link(href)).to_be_visible()


# ========== Юридические ссылки (href) ==========
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Юридические ссылки")
@allure.title("Ссылка «{name}» ведёт на URL по маске {href_re}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("name, href_re", [
    ("О компании", r"/ru/about/?$"),
    ("Соглашение об оказании услуг", r"/ru/terms/?$"),
    ("Политика конфиденциальности", r"/ru/privacy/?$"),
    ("Условия возврата", r"/ru/refund/?$"),
    ("Контакты", r"/ru/contacts/?$"),
])
def test_footer_legal_links_href(footer: FooterPage, name: str, href_re: str):
    with allure.step(f"Найти и проверить видимость ссылки «{name}»"):
        link = footer.get_legal_link_by_name(name)
        expect(link).to_be_visible()

    with allure.step("ссылка соответствует ожидаемому шаблону"):
        expect(link).to_have_attribute("href", re.compile(href_re))


# ========== Пустые ссылки ==========

@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("Пустые ссылки")
@allure.title("В футере нет пустых ссылок")
@allure.severity(allure.severity_level.MINOR)
def test_footer_has_no_empty_links(footer: FooterPage):
    expect(footer.empty_links).to_have_count(0)
