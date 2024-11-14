from datetime import datetime
from typing import List, Tuple

from fastapi import HTTPException

from src.core.models.shop_model import Product
from src.core.utils.logging_config import my_logger


def analyze_data(sales_data: List[Product]) -> tuple[int, str, str, datetime]:
    """
    Analyzes sales data to compute total revenue, top products sold, and distribution by categories.
    It needs for prompt query.

    This function iterates over a list of `Product` objects to calculate the total revenue,
    determine the top three products based on sales quantity, and produce a summary of sales
    distribution across different categories.

    :param sales_data: A list of Product objects, where each Product includes the `name`, `quantity`,
                       `price`, and `category` attributes.
    :type sales_data: List[Product]

    :return: A tuple containing:
        - Total revenue (int): The sum of the product of quantity and price for all products.
        - Top products (str): A formatted string of the top 3 products by sales quantity,
          each with its name and quantity sold.
        - Categories distribution (str): A formatted string showing the quantity sold for each category.
    :rtype: Tuple[int, str, str]

    :raises ValueError: If the sales_data list is empty.
    """
    if not sales_data:
        my_logger.info("Data is empty.")
        raise HTTPException(status_code=404, detail="Data is empty.")

    date: datetime = sales_data[0].date
    total_revenue = 0
    product_sales = {}
    category_distribution = {}

    for value in sales_data:
        total_revenue += value.quantity * value.price

        if value.name in product_sales:
            product_sales[value.name] += value.quantity
        else:
            product_sales[value.name] = value.quantity

        if value.category in category_distribution:
            category_distribution[value.category] += value.quantity
        else:
            category_distribution[value.category] = value.quantity

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
    return total_revenue, top_products_str, categories_str, date
