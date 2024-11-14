from typing import Any

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.shop_model import Product
from src.core.schemas.schemas import ProductBase
from src.core.utils.logging_config import my_logger


async def create_new_products(
    session: AsyncSession,
    data: list[dict[str, Any]],
) -> list[Product]:
    """
    Create new products
    :param session: connection to Postgres
    :param data: data to create new products
    :return: list[Product]
    """
    try:
        product_data = list()
        for product in data:
            model_dict = ProductBase.model_validate(product)
            product_data.append(Product(**model_dict.dict()))

        session.add_all(product_data)
        await session.commit()
    except Exception as e:
        my_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    my_logger.info(f"Created {len(data)} products")
    return product_data
