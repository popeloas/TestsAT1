# pages/google_page.py
from playwright.sync_api import Page
import time
import os


class GooglePage:
    """Простой класс для работы с Google."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.google.com"

    # Локаторы (CSS селекторы)
    SEARCH_INPUT = "textarea[name='q'], input[name='q']"
    SEARCH_BUTTON = "input[name='btnK']"
    LOGO = "img[alt='Google']"
    FIRST_RESULT = "div#search .g:first-child"
    ACCEPT_BUTTON = "button:has-text('Принять все'), button:has-text('Accept all')"

    def open(self):
        """Открыть Google."""
        self.page.goto(self.url)
        time.sleep(1)  # Простая пауза
        print(f"✓ Открыли Google")
        return self

    def accept_cookies(self):
        """Принять cookies, если есть кнопка."""
        try:
            button = self.page.locator(self.ACCEPT_BUTTON)
            if button.count() > 0 and button.first.is_visible(timeout=3000):
                button.first.click()
                print("✓ Приняли cookies")
                time.sleep(0.5)
        except:
            pass  # Если кнопки нет, ничего не делаем
        return self

    def search(self, text: str):
        """Выполнить поиск."""
        # Находим поле ввода
        search_box = self.page.locator(self.SEARCH_INPUT)
        search_box.wait_for(state="visible")

        # Вводим текст
        search_box.click()
        search_box.fill(text)
        print(f"✓ Ввели запрос: '{text}'")

        # Нажимаем Enter
        search_box.press("Enter")
        print("✓ Нажали Enter")

        # Ждем результаты
        time.sleep(2)
        return self

    def get_title(self) -> str:
        """Получить заголовок страницы."""
        return self.page.title()

    def get_url(self) -> str:
        """Получить текущий URL."""
        return self.page.url

    def take_screenshot(self, name: str = "screenshot"):
        """Сделать скриншот."""
        # Создаем папку если нет
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        # Имя файла с датой
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"

        # Делаем скриншот
        self.page.screenshot(path=path, full_page=True)
        print(f"📸 Скриншот: {path}")
        return path

    def is_logo_visible(self) -> bool:
        """Виден ли логотип."""
        try:
            logo = self.page.locator(self.LOGO)
            return logo.is_visible(timeout=3000)
        except:
            return False

    def has_results(self) -> bool:
        """Есть ли результаты поиска."""
        try:
            results = self.page.locator(self.FIRST_RESULT)
            return results.is_visible(timeout=5000)
        except:
            return False