from playwright.sync_api import Locator, expect
from pages.base_page import BasePage
import re
import allure



class HomePage(BasePage):

    # ============Locators
    @property
    def check_logo(self) -> Locator:
        return self.page.get_by_role("link", name="DV Jobs")

    @property
    def check_dipcoin(self) -> Locator:
        return self.page.get_by_role("link", name="DIPcoin")

    @property
    def lang_button(self) -> Locator:
        return self.page.get_by_role("button", name="Язык")

    @property
    def kz_language_item(self) -> Locator:
        return self.page.get_by_role("button", name="Қазақша KZ")

    @property
    def en_language_item(self) -> Locator:
        return self.page.get_by_role("button", name="English EN")

    @property
    def find_job(self) -> Locator:
        return self.page.locator("[data-test=\"home-button-create-resume\"]")

    @property
    def find_employee(self) -> Locator:
        return self.page.locator("[data-test=\"home-button-create-vacancy\"]")

    @property
    def new_resumes(self) -> Locator:
        return self.page.get_by_role("link", name="Создать резюме")


    @property
    def vacancies_button(self) -> Locator:
        return self.page.locator("button:has-text('Вакансии')").first

    @property
    def search_input(self) -> Locator:
        return self.page.get_by_placeholder(re.compile("Введите специальность", re.I))

    @property
    def search_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile("поиск", re.I))

    @property
    def vacancy_results(self) -> Locator:
        return self.page.locator("[class*='vacan'], [class*='card']")

    @property
    def resumes_button(self) -> Locator:
        return self.page.locator("button:has-text('Резюме')").first

    @property
    def resume_results(self) -> Locator:
        return self.page.locator("[class*='resume'], [class*='card'], [class*='item']")

    @property
    def img_accounting(self) -> Locator:
        return self.page.get_by_role("img", name="Бухгалтерское сопровождение и консультации")

    @property
    def img_legal(self) -> Locator:
        return self.page.get_by_role("img", name="Юридическое сопровождение и консультации")

    @property
    def img_hr_support(self) -> Locator:
        return self.page.get_by_role("img", name="Поддержка HR")

    @property
    def img_contracts(self) -> Locator:
        return self.page.get_by_role("img", name="оформление договоров на работу под ключ")

    @property
    def img_hiring(self) -> Locator:
        return self.page.get_by_role(
            "img",
            name="Помощь в найме сотрудников со всего мира и в оформлении миграционных документов",
        )

    @property
    def promotions(self) -> Locator:
        return self.page.get_by_role("link", name="Акции", exact=True)

    # ========== Чат поддержки

    @property
    def chat_widget_button(self) -> Locator:
        return self.page.locator(".support-chat-widget__button")

    @property
    def chat_widget_container(self) -> Locator:
        return self.page.locator(".support-chat-widget__container")

    # ========== Меню «Соискателям» ==========

    @property
    def candidates_menu_button(self) -> Locator:
        return self.page.get_by_role("button", name="Соискателям")

    @property
    def vacancies_catalog_link(self) -> Locator:
        return self.page.get_by_role("link", name="Каталог вакансий")

    @property
    def interview_tips_link(self) -> Locator:
        return self.page.get_by_role("link", name="Советы прохождения интервью")

    @property
    def contract_link(self) -> Locator:
        return self.page.get_by_role("link", name="Заключение договора")

    @property
    def lawyer_consult_link(self) -> Locator:
        return self.page.get_by_role("link", name="Консультация юриста")

    @property
    def accountant_consult_link(self) -> Locator:
        return self.page.get_by_role("link", name="Консультация бухгалтера")


    # ========== Меню «Работодателям»

    @property
    def employers_menu_button(self) -> Locator:
        return self.page.get_by_role("button", name="Работодателям")

    @property
    def resumes_catalog_link(self) -> Locator:
        return self.page.get_by_role("link", name="Каталог резюме")

    @property
    def employer_contract_link(self) -> Locator:
        return self.page.get_by_role("link", name="Заключение договора")

    @property
    def employer_lawyer_consult_link(self) -> Locator:
        return self.page.get_by_role("link", name="Консультация сопровождение юриста")

    @property
    def employer_accountant_consult_link(self) -> Locator:
        return self.page.get_by_role("link", name="Консультация сопровождение бухгалтера")

    @property
    def hiring_help_link(self) -> Locator:
        return self.page.get_by_role("link", name="Помощь в найме сотрудников")

    @property
    def migration_docs_link(self) -> Locator:
        return self.page.get_by_role("link", name="Помощь в оформлении миграционных документов")

        # ========= Actions

    @allure.step("Клик по логотипу DV Jobs")
    def click_logo(self) -> None:
        self.check_logo.click()

    @allure.step("Клик по ссылке DIPcoin")
    def click_dipcoin(self) -> None:
        self.check_dipcoin.click()

    @allure.step("Открытие дропдауна выбора языка")
    def open_language_dropdown(self) -> None:
        """Открывает дропдаун языка с ожиданием гидратации."""
        self.lang_button.wait_for(state="visible")
        for _ in range(10):
            self.lang_button.click()
            try:
                expect(self.lang_button).to_have_attribute(
                    "aria-expanded", "true", timeout=1000
                    )
                break
            except AssertionError:
                self.page.wait_for_timeout(500)
            else:
                raise AssertionError(
                    "Дропдаун языка не открылся — гидратация не завершилась"
                )

    @allure.step("Переключение на казахский язык (KZ)")
    def select_kz_language(self) -> None:
        """Выбирает казахский язык в дропдауне."""
        self.open_language_dropdown()
        expect(self.kz_language_item).to_be_visible(timeout=5000)
        self.kz_language_item.click()
        self.page.wait_for_url("https://dvjob.kz/kz", wait_until="domcontentloaded")

    @allure.step("Переключение на английский язык (EN)")
    def select_en_language(self) -> None:
        """Выбирает английский язык."""
        self.open_language_dropdown()
        expect(self.en_language_item).to_be_visible(timeout=5000)
        self.en_language_item.click()
        self.page.wait_for_url("https://dvjob.kz/en", wait_until="domcontentloaded")

    @allure.step("Клик по кнопке «Найти работу»")
    def click_find_job(self) -> None:
        self.find_job.click()

    @allure.step("Клик по кнопке «Найти сотрудника»")
    def click_find_employee(self) -> None:
        self.find_employee.click()

    @allure.step("Клик по кнопке «Создать резюме»")
    def click_new_resumes(self) -> None:
        self.new_resumes.click()

    @allure.step("Поиск вакансий по запросу: '{query}'")
    def search_vacancies(self, query: str) -> None:
        """Переходит в раздел вакансий и выполняет поиск."""
        self.vacancies_button.click()
        self.search_input.fill(query)
        self.search_button.click()
        expect(self.vacancy_results.first).to_be_visible(timeout=30_000)

    @allure.step("Поиск резюме по запросу: '{query}'")
    def search_resumes(self, query: str) -> None:
        """Переходит в раздел резюме и выполняет поиск."""
        self.resumes_button.click()
        self.search_input.fill(query)
        self.search_button.click()

    @allure.step("Проверка видимости изображений блока услуг")
    def check_services_images(self) -> None:
        """Проверяет видимость всех изображений блока услуг."""
        for img in (
        self.img_accounting,
        self.img_legal,
        self.img_hr_support,
        self.img_contracts,
        self.img_hiring,
            ):
            expect(img).to_be_visible()

    @allure.step("Переход на страницу «Акции»")
    def click_promotions(self) -> None:
        """Переходит на страницу акций."""
        self.promotions.wait_for(state="visible")
        self.promotions.click()
        self.page.wait_for_url("**/promotions", wait_until="domcontentloaded")

    @allure.step("Открытие виджета чата поддержки")
    def open_chat_support(self) -> None:
        """Открывает виджет чата поддержки."""
        self.chat_widget_button.click()

        # ========== Меню «Соискателям» ==========

    @allure.step("Открытие дропдауна меню «Соискателям»")
    def open_candidates_dropdown(self) -> None:
        """Открывает дропдаун «Соискателям» с защитой от гидратации."""
        self.candidates_menu_button.wait_for(state="visible")
        for _ in range(10):
            self.candidates_menu_button.click(no_wait_after=True)
            try:
                expect(self.candidates_menu_button).to_have_attribute(
                    "aria-expanded", "true", timeout=1000
                )
                break
            except AssertionError:
                    self.page.wait_for_timeout(500)
            else:
                raise AssertionError(
                    "Дропдаун «Соискателям» не открылся — гидратация не завершилась"
                )

    @allure.step("Переход в каталог вакансий (меню соискателя)")
    def click_vacancies_catalog(self) -> None:
        """Переход в каталог вакансий через меню соискателя."""
        self.open_candidates_dropdown()
        self.vacancies_catalog_link.click()

    @allure.step("Переход к советам по прохождению интервью")
    def click_interview_tips(self) -> None:
        """Открывает советы по прохождению интервью."""
        self.open_candidates_dropdown()
        self.interview_tips_link.click()

    @allure.step("Переход к форме заключения договора (соискатель)")
    def click_contract(self) -> None:
        """Открывает форму заключения договора."""
        self.open_candidates_dropdown()
        self.contract_link.click()

    @allure.step("Переход к консультации юриста (соискатель)")
    def click_lawyer_consult(self) -> None:
        """Переход к консультации юриста."""
        self.open_candidates_dropdown()
        self.lawyer_consult_link.click()

    @allure.step("Переход к консультации бухгалтера (соискатель)")
    def click_accountant_consult(self) -> None:
        """Переход к консультации бухгалтера."""
        self.open_candidates_dropdown()
        self.accountant_consult_link.click()

        # ========== Меню «Работодателям» ==========

    @allure.step("Открытие дропдауна меню «Работодателям»")
    def open_employers_dropdown(self) -> None:
        """Открывает дропдаун «Работодателям» с защитой от гидратации."""
        self.employers_menu_button.wait_for(state="visible")
        for _ in range(10):
            self.employers_menu_button.click(no_wait_after=True)
            try:
                expect(self.employers_menu_button).to_have_attribute(
                    "aria-expanded", "true", timeout=1000
                )
                break
            except AssertionError:
                    self.page.wait_for_timeout(500)
            else:
                raise AssertionError(
                    "Дропдаун «Работодателям» не открылся — гидратация не завершилась"
                )

    @allure.step("Переход в каталог резюме (меню работодателя)")
    def click_resumes_catalog(self) -> None:
        """Переход в каталог резюме через меню работодателя."""
        self.open_employers_dropdown()
        self.resumes_catalog_link.click()

    @allure.step("Переход к форме заключения договора (работодатель)")
    def click_employer_contract(self) -> None:
        """Открывает форму заключения договора (работодатель)."""
        self.open_employers_dropdown()
        self.employer_contract_link.click()

    @allure.step("Переход к консультации юриста (работодатель)")
    def click_employer_lawyer_consult(self) -> None:
        """Переход к консультации юриста (работодатель)."""
        self.open_employers_dropdown()
        self.employer_lawyer_consult_link.click()

    @allure.step("Переход к консультации бухгалтера (работодатель)")
    def click_employer_accountant_consult(self) -> None:
        """Переход к консультации бухгалтера (работодатель)."""
        self.open_employers_dropdown()
        self.employer_accountant_consult_link.click()

    @allure.step("Переход к помощи в найме сотрудников")
    def click_hiring_help(self) -> None:
        """Переход к помощи в найме сотрудников."""
        self.open_employers_dropdown()
        self.hiring_help_link.click()

    @allure.step("Переход к помощи в оформлении миграционных документов")
    def click_migration_docs(self) -> None:
        """Переход к помощи в оформлении миграционных документов."""
        self.open_employers_dropdown()
        self.migration_docs_link.click()