import pytest
from playwright.sync_api import Page, expect


class TestAuthorization:
    """Тесты авторизации"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Подготовка перед каждым тестом"""
        page.goto("https://lkb-temp-kub.smbconnect.ru/login")

    def login(self, username: str, password: str, page: Page):
        """Вспомогательный метод для авторизации"""
        page.locator("#basic_username").fill(username)
        page.locator("#basic_password").fill(password)
        page.get_by_role("button", name="Войти").click()

    def test_select_task_action(self, page: Page):
        # Авторизуемся
        self.login("admin@test.ru", "test", page)
        expect(page).to_have_url("https://lkb-temp-kub.smbconnect.ru/tasks")

        # Переход на страницу задачи
        page.goto("https://lkb-temp-kub.smbconnect.ru/task/db8fa434-f15d-4dc3-907e-bd2e8e510e3e")
        page.wait_for_load_state("networkidle", timeout=15000)

        # Отладка: выводим все селекты на странице
        selects = page.locator(".ant-select").all()
        print(f"\nНайдено селектов: {len(selects)}")

        # Отладка: выводим все ID на странице
        all_ids = page.locator("[id]").all()
        for element in all_ids[:10]:  # Первые 10 элементов с ID
            try:
                element_id = element.get_attribute("id")
                print(f"ID: {element_id}")
            except:
                pass

        # Пробуем разные варианты селекторов
        try:
            # Вариант 1: По ID
            select = page.locator("#taskActionSelectId")
            if select.count() > 0:
                print("Найден по ID")
        except:
            # Вариант 2: По классу и тексту
            select = page.locator(".ant-select").first
            print("Используем первый .ant-select")

        # Делаем скриншот для отладки
        page.screenshot(path="debug_screenshot.png")

        # Проверяем что селект существует
        expect(select).to_be_visible(timeout=10000)

        # Открываем селект
        select.click()

        # Ждем dropdown
        expect(page.locator(".ant-select-dropdown:visible")).to_be_visible(timeout=5000)

        # Выбираем опцию
        page.locator(".ant-select-dropdown").get_by_text("Завершить задачу").click()

        # Проверка
        expect(select).to_contain_text("Завершить задачу", timeout=5000)

        # Подтверждаем действие
        page.get_by_role("button", name="Подтвердить").click()

        # Проверяем, что выбранное действие отображается
        expect(page.locator("div.ant-select")).to_contain_text("Завершить задачу")