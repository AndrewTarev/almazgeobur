from datetime import datetime
from typing import List, Any, Tuple

from celery import chain
from fastapi import APIRouter, UploadFile, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.cruds.product_crud import create_new_products
from src.celery.celery_worker import task_generate_and_save_report, task_analyze_data
from src.core.db_helper import db_helper
from src.core.models.shop_model import Product
from src.core.schemas.schemas import ProductOut
from src.core.utils.data_analyzer import analyze_data
from src.core.utils.logging_config import my_logger
from src.core.utils.xml_parser import parse_xml


router = APIRouter()


@router.post(
    "/parse-xml/",
    response_model=List[ProductOut],
    status_code=status.HTTP_201_CREATED,
)
async def parse_xml_endpoint(
    file: UploadFile,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[Product]:
    content = await file.read()
    dict_data: list[dict[str, Any]] = parse_xml(content)
    products_list: List[Product] = await create_new_products(
        session=session, data=dict_data
    )
    # Создание и выполнение цепочки задач
    result = chain(task_analyze_data.s(dict_data) | task_generate_and_save_report.s())()
    # total_revenue, top_products_str, categories_str, date = analyze_data(products_list)
    # report = task_generate_and_save_report.delay(
    #     date=date,
    #     total_revenue=total_revenue,
    #     top_products=top_products_str,
    #     categories=categories_str,
    # )
    return products_list
