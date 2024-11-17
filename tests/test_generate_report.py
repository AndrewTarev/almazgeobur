import pytest
from unittest.mock import patch, Mock

from src.core.config import settings

from src.core.utils.sales_data_prompt import generate_report_content


# Замокировать клиент OpenAI
@pytest.fixture
def mock_openai():
    with patch("src.core.utils.sales_data_prompt.OpenAI") as MockOpenAI:
        yield MockOpenAI


def test_generate_report_content_success(mock_openai):
    # Создаем мока для результата, который вернет наш фейковый клиент OpenAI
    mock_completion_response = Mock()
    mock_completion_response.choices = [
        Mock(message=Mock(content="This is a generated report."))
    ]

    # Настраиваем мок-клиент OpenAI так, чтобы возвращать подготовленное завершение
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = mock_completion_response

    # Определяем входные данные
    date = "2023-10-10"
    total_revenue = 10000
    top_products = "ProductA (20), ProductB (15), ProductC (10)"
    categories = "Category1: 30, Category2: 15"

    # Вызываем тестируемую функцию
    report = generate_report_content(date, total_revenue, top_products, categories)

    # Проверяем, что функция возвращает ожидаемый результат
    assert report == "This is a generated report."

    # Проверяем, что метод completions.create был вызван с нужными параметрами
    expected_prompt = f"""
    Проанализируй данные о продажах за {date}:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {top_products}
    3. Распределение по категориям: {categories}

    Составь краткий аналитический отчет с выводами и рекомендациями.
    """
    mock_client.chat.completions.create.assert_called_once_with(
        model=settings.openapi.openai_gpt_model,
        messages=[{"role": "user", "content": expected_prompt}],
    )


def test_generate_report_content_failure(mock_openai):
    # Настраиваем мок-клиент OpenAI так, чтобы выбрасывать ошибку
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.side_effect = Exception("API error")

    # Определяем входные данные
    date = "2023-10-10"
    total_revenue = 10000
    top_products = "ProductA (20), ProductB (15), ProductC (10)"
    categories = "Category1: 30, Category2: 15"

    # Ловим и проверяем выброс исключения
    with pytest.raises(Exception) as exc_info:
        generate_report_content(date, total_revenue, top_products, categories)

    assert str(exc_info.value) == "API error"
