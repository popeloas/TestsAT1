# conftest.py
import pytest
from playwright.sync_api import Browser, Page


@pytest.fixture(scope="session")
def browser():
    """Запускаем браузер один раз для всех тестов."""
    from playwright.sync_api import sync_playwright

    # Используем with для автоматического закрытия
    with sync_playwright() as playwright:
        # Запускаем браузер
        browser = playwright.chromium.launch(
            headless=False,  # Браузер виден (для отладки)
            slow_mo=100,  # Замедляем действия (как человек)
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    """Создаем новую страницу для каждого теста."""
    # Создаем контекст
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="ru-RU",  # Русский язык
    )

    # Создаем страницу
    page = context.new_page()

    # Устанавливаем время ожидания
    page.set_default_timeout(10000)  # 10 секунд

    # Добавляем обработчик для скриншотов при падении теста
    def take_screenshot_on_failure():
        import os
        from datetime import datetime

        # Создаем папку для скриншотов
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        # Делаем скриншот при ошибке
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/error_{timestamp}.png")
        print(f"📸 Скриншот сохранен: screenshots/error_{timestamp}.png")

    # Сохраняем оригинальный метод
    original_close = page.close

    def close_with_screenshot():
        # Если страница еще открыта, можно сделать что-то перед закрытием
        if not page.is_closed():
            pass
        original_close()

    page.close = close_with_screenshot

    yield page

    # Закрываем страницу и контекст после теста
    page.close()
    context.close()