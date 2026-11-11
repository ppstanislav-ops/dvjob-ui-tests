# DVJob UI Tests

Автоматизированный фреймворк UI-тестирования для международной платформы по поиску работы (https://dvjob.kz).
Навигация, поиск, авторизация двух ролей и серверная валидация логина, включая негативные и security-сценарии.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![pytest](https://img.shields.io/badge/pytest-9.x-green)
![Playwright](https://img.shields.io/badge/Playwright-1.64-orange)
![Allure](https://img.shields.io/badge/Allure-2.16-purple)

## Чем интересен проект

- **Page Object Model** с role-based локаторами (`get_by_role`, `get_by_placeholder`) —
  устойчивыми к изменениям вёрстки.
- **Перехват и подмена сетевых запросов** (`page.route` + `expect_response`):
  фронт отправляет валидный email, перехват подменяет поле `username` — так
  проверяется именно серверная валидация, а не клиентская.
- **Security-кейсы в параметризации**: SQL-инъекция, XSS, омоглифы,
  10 000 символов, пустые значения — единый сценарий × две роли.
- **Управление известной уязвимостью через `xfail(strict=True)`**: пока бэкенд
  не починил null-byte обход, тест «ожидаемо падает» и CI зелёный; после фикса
  тест станет XPASS и сам напомнит снять метку.
- **Развёрнутые Allure-отчёты**: `environment.properties`, `executor.json`
  с инкрементным buildOrder для вкладки Trends, свои категории дефектов,
  скриншот + HTML + URL страницы автоматически прикладываются к упавшему тесту.
- **Ретраи на гидратацию Nuxt/Vue**: клики по ролям и дропдаунам повторяются
  до подтверждения (`aria-expanded`, активный класс) вместо слепых `sleep`.
- **Единая конфигурация** (`config.py` + `.env`): адрес стенда и креды не
  хардкодятся и не попадают в репозиторий.

## 📸 Скриншоты Allure-отчёта

Ниже приведены примеры сгенерированных Allure-отчётов с результатами прогона.

**Обзор (Overview):**
Наглядно видно 100% прохождение (20 passed, 2 skipped), а также Environment с информацией о стенде и браузере.
![Allure Overview](docs/allure/01-overview.png)

**Детализация тестов (Suites):**
Древовидная структура с шагами, приложенными параметрами (payload'ы, ожидаемые статусы) и вложениями.
![Allure Suites](docs/allure/02-suites.png)

**Графики (Graphs):**
Распределение тестов по статусам, уровням критичности (Severity) и длительности.
![Allure Graphs](docs/allure/03-graphs.png)

##  Технологии

- **Python 3.12+**
- **Playwright** — браузерная автоматизация (Chromium)
- **pytest** — тестовый runner
- **pytest-playwright** — интеграция Playwright с pytest
- **pytest-rerunfailures** — один ретрай для flaky-тестов (`--reruns 1`)
- **Allure Framework** — HTML-отчётность с шагами, скриншотами и аттачами
- **python-dotenv** — хранение учётных данных в `.env`

## Покрытие (64 кейса)

| Модуль | Кейсов | Что проверяется |
| --- | ---: | --- |
| `test_main_page.py` | 13 | заголовок, логотип, переключение языков, поиск вакансий/резюме, промо, чат поддержки |
| `test_upper_menu.py` | 6 | меню «Соискателям» и «Работодателям»: каталоги, советы, формы, авторизация для консультаций |
| `test_footer.py` | 21 | ссылки, телефон/e-mail, адрес, копирайт, соцсети, отсутствие пустых `href` |
| `test_auth.py` | 4 | вход соискателя и работодателя (позитив/негатив) |
| `test_server_validation.py` | 22 | серверная валидация `username` (10 значений × 2 роли) + 2 null-byte уязвимости |

## 📁 Структура проекта

```

├── conftest.py                     # фикстуры (home/footer/auth/validation_page),
│                                   # автоскриншот при падении, генерация environment.properties/
│                                   # executor.json/categories.json для Allure
├── pytest.ini                      # конфиг pytest: --alluredir, --reruns 1
├── requirements.txt                # прямые зависимости
├── .env.example                    # шаблон учётных данных (нужно скопировать в .env)
├── pages/                          # Page Object Layer
│   ├── base_page.py                # базовый класс страницы
│   ├── home_page.py                # главная страница (лого, язык, поиск, меню)
│   ├── footer_page.py              # футер (контакты, ссылки, соцсети)
│   ├── auth_page.py                # страница авторизации (роли, форма, валидация)
│   └── server_validation_page.py   # перехват запроса /v1/accounts/sign-in с подменой username
├── tests/                          # тестовые модули
│   ├── test_main_page.py
│   ├── test_footer.py
│   ├── test_upper_menu.py
│   ├── test_auth.py
│   ├── test_request_candidate.py  # security-валидация (соискатель)
│   └── test_request_employer.py   # security-валидация (работодатель)
└── docs/allure/                    # скриншоты Allure-отчёта для README
```

## 🚀 Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
git clone <repo-url>
cd <project>

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Подготовка учётных данных

```bash
cp .env.example .env
# Откройте .env и впишите валидные логины/пароли тестовых аккаунтов dvjob.kz:
#   CandidateLogin, CandidatePassword       — тестовый аккаунт соискателя
#   EmployerLogin, EmployerPassword          — тестовый аккаунт работодателя
```

### 3. Запуск тестов

```bash
# Весь набор
pytest

# Один модуль
pytest tests/test_footer.py

# Один тест с подробным выводом
pytest tests/test_footer.py::test_footer_phone -v
```

### 4. Просмотр Allure-отчёта

```bash
allure serve allure-results
# или:
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## 🧠 Ключевые инженерные решения

### Page Object Model
Каждая страница инкапсулирована в свой класс (`HomePage`, `FooterPage`, `AuthPage`, `ServerValidationAuthPage`). Локаторы вынесены в `@property`, действия — в методы с `@allure.step`. Это даёт читаемый отчёт и устойчивость к изменениям вёрстки.

### Защита от «гидратации» Vue/Nuxt
На дропдаунах (язык, «Соискателям», «Работодателям») используется retry-цикл с проверкой `aria-expanded="true"` вместо фиксированного `wait_for_timeout` — клики не «глотаются» при медленном монтировании Vue.

### Серверная валидация через route-interception
В `ServerValidationAuthPage.setup_username_interception()` регистрируется `page.route(...)` на `/v1/accounts/sign-in`. Фронт всегда отправляет валидный email через форму; перехват подменяет поле `username` в JSON-теле на подозрительное значение. Так проверяется именно серверная валидация, а не фронтовая.

### Security-кейсы (10 параметризованных + 1 known-vulnerability)
- Несуществующий / неформатный / омоглифный email → `404 account_not_found`
- SQL-инъекция (`' OR 1=1 --`) → `404 account_not_found`
- XSS-payload (`<script>alert(1)</script>`) → `404 account_not_found`
- Превышение длины username (10 000 символов) → `404 account_not_found`
- Пустой / только пробелы → `422 validation_error`
- **Null byte injection** (`<valid_email>\x00`) — известная уязвимость, помечена `@pytest.mark.xfail(strict=True)`: пока не пофикшена — тест «ожидаемо падает», после фикса бэкенда `strict=True` превратит XPASS в падение с подсказкой «убери `@xfail`».

### Allure-интеграция
- `pytest_sessionfinish` генерирует `environment.properties` (Base URL, браузер, стенд, Python, OS), `executor.json` (build name/order) и `categories.json` (Баги продукта / Проблемы теста / Skipped).
- `.build_order` — сквозной номер билда, чтобы во вкладке **Trends** были разные точки.
- `screenshot_on_failure` — автоскриншот, HTML и URL страницы при падении теста.

### Ретраи
`pytest.ini` → `--reruns 1` (через `pytest-rerunfailures`): один ретрай для устойчивости к flaky на production-стенде.

---

## 🔐 Безопасность

- Все учётные данные хранятся в `.env`, который **игнорируется git** (см. `.gitignore`).
- В репозитории лежит только `.env.example` с шаблонами переменных.
- Реальные креды от тестовых аккаунтов в репозиторий не попадают.

---

## 🌍 Окружение

- **Base URL:** https://dvjob.kz
- **Браузер:** Chromium (Playwright)
- **Стенд:** production
- **OS:** Windows 11 (локальный прогон), совместимо с Linux/macOS

---

## 📄 Лицензия

Проект предоставляется в учебно-портфолийных целях. См. `LICENSE` (MIT) прилагается.