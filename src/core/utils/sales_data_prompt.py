from openai import OpenAI

from src.core.config import settings
from src.core.utils.logging_config import my_logger


def generate_report_content(
    date: str, total_revenue: float, top_products: str, categories: str
) -> str | None:
    """
    Генерирует аналитический отчет на основе предоставленных данных о продажах.

    :param date: Дата отчета.
    :param total_revenue: Общая выручка за период.
    :param top_products: Список топ-3 товаров по продажам.
    :param categories: Список категорий с их долей в продажах.
    :return: Сгенерированный текст аналитического отчета.
    """
    my_logger.debug("Starting generate_report_content.")

    prompt = f"""
    Проанализируй данные о продажах за {date}:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {top_products}
    3. Распределение по категориям: {categories}

    Составь краткий аналитический отчет с выводами и рекомендациями.
    """
    try:
        client = OpenAI(
            api_key=settings.openapi.openai_api_key,
            base_url=settings.openapi.openai_base_url,
        )
        completion = client.chat.completions.create(
            model=settings.openapi.openai_gpt_model,
            messages=[{"role": "user", "content": prompt}],
        )
        report_content = completion.choices[0].message.content

    except Exception as e:
        my_logger.error(f"Error in OpenAI completion: {str(e)}")
        raise Exception(e)
    my_logger.info("Prompt query completed successfully.")
    return report_content
