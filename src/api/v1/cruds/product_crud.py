from typing import Any, List

from src.core.db_helper import db_helper
from src.core.models.shop_model import Product, LLMreport
from src.core.schemas.schemas import ProductBase
from src.core.utils.logging_config import my_logger


async def create_new_products_and_report(
    ai_report: str,
    data: List[ProductBase],
) -> list[Product]:
    """
    Записывает в БД products и LLM
    :param ai_report: Отчет LLM
    :param data: список словарей из XML файла
    :return: list[Product]
    """
    try:
        async with db_helper.session_factory() as session:
            # Запись отчета в БД
            report = LLMreport(ai_report=ai_report)
            session.add(report)
            await session.flush()
            # Получаем id отчета
            report_id = report.id

            # Записываем данные из XML в БД
            product_data = list()
            for product in data:
                model_dict = ProductBase.model_validate(product)
                product_data.append(
                    Product(
                        name=model_dict.name,
                        report_id=report_id,
                        price=model_dict.price,
                        quantity=model_dict.quantity,
                        category=model_dict.category,
                        date=model_dict.date,
                    )
                )

            session.add_all(product_data)
            await session.commit()
    except Exception as e:
        await session.rollback()
        my_logger.error(str(e))
    my_logger.info(f"Created {len(data)} products in database")
    return product_data
