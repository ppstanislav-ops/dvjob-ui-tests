import  allure
from playwright.sync_api import Locator
from pages.base_page import BasePage


class FooterPage(BasePage):

    # ========== Locators==========

    @property
    def footer(self) -> Locator:
        return self.page.locator("footer").first

    @property
    def address_text(self) -> Locator:
        return self.footer.get_by_text("Адрес: г.Алматы, пр. Достык 202, оф.")

    @property
    def about_link(self) -> Locator:
        return self.footer.get_by_role("link", name="О компании")

    @property
    def terms_link(self) -> Locator:
        return self.footer.get_by_role("link", name="Соглашение об оказании услуг")

    @property
    def privacy_link(self) -> Locator:
        return self.footer.get_by_role("link", name="Политика конфиденциальности")

    @property
    def refund_link(self) -> Locator:
        return self.footer.get_by_role("link", name="Условия возврата")

    @property
    def contacts_link(self) -> Locator:
        return self.footer.get_by_role("link", name="Контакты")

    @property
    def phone_link(self) -> Locator:
        return self.footer.locator('a[href^="tel:"]').first

    @property
    def email_link(self) -> Locator:
        return self.footer.locator('a[href^="mailto:"]').first

    @property
    def copyright_text(self) -> Locator:
        return self.footer.get_by_text("ТОО «DVjob»")

    @property
    def legal_notice_text(self) -> Locator:
        return self.footer.get_by_text("рекомендательные технологии")

    @property
    def empty_links(self) -> Locator:
        return self.footer.locator('a[href="#"], a:not([href])')


    def get_social_link(self, href: str) -> Locator:
        return self.footer.locator(f'a[href="{href}"]')


    def get_legal_link_by_name(self, name: str) -> Locator:
        return self.footer.get_by_role("link", name=name)

    # ========== Actions ==========

    @allure.step("Переход на страницу «О компании»")
    def click_about(self) -> None:
        self.about_link.click()

    @allure.step("Переход на страницу «Соглашение об оказании услуг»")
    def click_terms(self) -> None:
        self.terms_link.click()

    @allure.step("Переход на страницу «Политика конфиденциальности»")
    def click_privacy(self) -> None:
        self.privacy_link.click()

    @allure.step("Переход на страницу «Условия возврата»")
    def click_refund(self) -> None:
        self.refund_link.click()

    @allure.step("Переход на страницу «Контакты»")
    def click_contacts(self) -> None:
        self.contacts_link.click()

