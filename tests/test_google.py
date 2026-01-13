# tests/test_google.py
import pytest
from pages.google_page import GooglePage


def test_open_google(page):
    """Тест 1: Просто открываем Google."""
    print("\n" + "=" * 50)
    print("ТЕСТ 1: Открываем Google")
    print("=" * 50)

    # Создаем объект страницы
    google = GooglePage(page)

    # Открываем Google
    google.open()

    # Принимаем cookies
    google.accept_cookies()

    # Проверяем логотип
    if google.is_logo_visible():
        print("✓ Логотип виден")
    else:
        print("⚠ Логотип не найден")

    # Проверяем заголовок
    title = google.get_title()
    print(f"Заголовок: {title}")

    # Делаем скриншот
    google.take_screenshot("test1_main_page")

    # Проверка
    assert "Google" in title
    print("✅ ТЕСТ 1 ПРОЙДЕН!")


def test_search_in_google(page):
    """Тест 2: Поиск в Google."""
    print("\n" + "=" * 50)
    print("ТЕСТ 2: Поиск в Google")
    print("=" * 50)

    google = GooglePage(page)

    # Открываем и ищем
    google.open().accept_cookies().search("Python programming")

    # Проверяем результаты
    if google.has_results():
        print("✓ Результаты поиска найдены")
    else:
        print("⚠ Результаты не найдены")

    # Проверяем заголовок
    title = google.get_title()
    print(f"Заголовок после поиска: {title}")

    # Скриншот
    google.take_screenshot("test2_search_results")

    # Простая проверка
    assert "Python" in title or "python" in title.lower()
    print("✅ ТЕСТ 2 ПРОЙДЕН!")


def test_multiple_searches(page):
    """Тест 3: Несколько поисковых запросов."""
    print("\n" + "=" * 50)
    print("ТЕСТ 3: Разные запросы")
    print("=" * 50)

    google = GooglePage(page)

    # Список запросов для теста
    queries = ["automation testing", "Playwright", "web development"]

    for query in queries:
        print(f"\n--- Ищем: '{query}' ---")

        # Для каждого запроса открываем новую страницу
        # (так надежнее, чтобы избежать блокировок)
        google.open().accept_cookies().search(query)

        # Делаем скриншот
        google.take_screenshot(f"test3_{query.replace(' ', '_')}")

        # Простая проверка
        assert query.split()[0].lower() in google.get_title().lower()

        # Пауза между запросами
        page.wait_for_timeout(1000)

    print("✅ ТЕСТ 3 ПРОЙДЕН!")


def test_check_page_elements(page):
    """Тест 4: Проверяем основные элементы на странице."""
    print("\n" + "=" * 50)
    print("ТЕСТ 4: Проверка элементов")
    print("=" * 50)

    google = GooglePage(page)
    google.open()

    # Проверяем разные типы элементов
    elements_to_check = [
        ("текстовое поле", "input[type='text'], textarea"),
        ("кнопка", "button, input[type='submit']"),
        ("ссылка", "a"),
        ("изображение", "img"),
    ]

    found_elements = []

    for element_name, selector in elements_to_check:
        count = page.locator(selector).count()
        if count > 0:
            print(f"✓ {element_name}: {count} шт")
            found_elements.append(element_name)
        else:
            print(f"✗ {element_name}: не найдено")

    # Успех если нашли хотя бы 3 типа элементов
    assert len(found_elements) >= 3, f"Нашли только {len(found_elements)} типа элементов"

    google.take_screenshot("test4_page_elements")
    print(f"✅ Найдены элементы: {', '.join(found_elements)}")
    print("✅ ТЕСТ 4 ПРОЙДЕН!")


# Опционально: тест с параметрами
@pytest.mark.parametrize("search_query", [
    "test automation",
    "software testing",
    "quality assurance"
])
def test_parametrized_search(page, search_query):
    """Тест 5: Поиск с разными параметрами."""
    print(f"\nТЕСТ 5: Ищем '{search_query}'")

    google = GooglePage(page)
    google.open().accept_cookies().search(search_query)

    # Простая проверка
    title = google.get_title()
    assert len(title) > 0  # Просто проверяем что заголовок не пустой

    google.take_screenshot(f"test5_{search_query.replace(' ', '_')}")
    print(f"✅ Поиск '{search_query}' выполнен успешно")