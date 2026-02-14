# Автотесты авторизации на Playwright

## Установка

1. Создайте виртуальное окружение:
``` pip install -r requirements.txt
playwright install
pytest
  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите браузеры для Playwright:
```bash
playwright install
```

## Настройка

Откройте файл `test_auth.py` и измените:
- URL вашего приложения (строка `page.goto(...)`)
- Селекторы полей ввода (например, `input[name="username"]`)
- Тестовые данные (логин и пароль)
- Ожидаемые результаты (URL после входа, текст сообщений)

## Запуск тестов

Запустить все тесты:
```bash
pytest
```

Запустить конкретный тест:
```bash
pytest test_auth.py::TestAuthorization::test_successful_login
```

Запустить в headless режиме (без GUI браузера):
```bash
pytest --headed=false
```

Запустить с генерацией HTML отчета:
```bash
pytest --html=report.html --self-contained-html
```

## Структура проекта

- `test_auth.py` - тесты авторизации
- `conftest.py` - фикстуры Playwright
- `pytest.ini` - конфигурация pytest
- `requirements.txt` - зависимости проекта

## Полезные команды

Запись теста в интерактивном режиме:
```bash
playwright codegen https://your-site.com
```

Отладка теста:
```bash
pytest --headed --slowmo=1000
```

## Примеры селекторов

```python
# По тексту
page.locator('text="Войти"')

# По роли
page.locator('role=button[name="Submit"]')

# CSS селектор
page.locator('#login-button')

# XPath
page.locator('xpath=//button[@type="submit"]')

# Комбинированный
page.locator('form >> button:has-text("Login")')
```
