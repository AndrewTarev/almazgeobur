from typing import Any
from src.core.utils.logging_config import my_logger


def analyze_data(sales_data: list[dict[str, Any]]) -> tuple:
    """
    Анализирует данные о продажах и возвращает сводку, включающую общую выручку,
    топовые продукты и категории.

    :param sales_data: Список словарей, каждый из которых представляет продажу.
                       Каждый словарь должен содержать ключи:
                       "name", "quantity", "price", "category", и "date".
    :return: Кортеж, содержащий:
         - дату первой записи из данных
         - общую выручку
         - строку с топ-3 продуктами и их количеством
         - строку с распределением по категориям и количеством продаж.
    """
    my_logger.debug("Task analyzing data started")

    if not sales_data:
        my_logger.info("Data is empty.")
        raise ValueError("Data is empty.")

    date = sales_data[0]["date"]
    total_revenue = 0
    product_sales = {}
    category_distribution = {}

    for sale in sales_data:
        total_revenue += sale["quantity"] * sale["price"]

        if sale["name"] in product_sales:
            product_sales[sale["name"]] += sale["quantity"]
        else:
            product_sales[sale["name"]] = sale["quantity"]

        if sale["category"] in category_distribution:
            category_distribution[sale["category"]] += sale["quantity"]
        else:
            category_distribution[sale["category"]] = sale["quantity"]

    # Определение топ-3 продуктов по продажам
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:3]

    # Формирование строк для промпта
    top_products_str = ", ".join(
        [f"{name} ({quantity})" for name, quantity in top_products]
    )
    categories_str = ", ".join(
        [f"{cat}: {qty}" for cat, qty in category_distribution.items()]
    )

    my_logger.info("Analyzing sales data successfully.")
    return date, total_revenue, top_products_str, categories_str
