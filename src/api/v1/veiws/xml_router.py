from datetime import date
from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.cruds.product_crud import OrmQuery
from src.core.db_helper import db_helper
from src.core.schemas.schemas import (
    AIReportResponse,
    ProductResponse,
    ParseEndpointResponse,
)
from src.core.utils.logging_config import my_logger


router = APIRouter()


@router.post(
    "/parse-xml/",
    response_model=ParseEndpointResponse,
    status_code=status.HTTP_201_CREATED,
)
async def parse_xml_endpoint(
    file: UploadFile,
):
    """
    Принимает XML файл, создает цепочку фоновых задач в Celery.
    Цепочка задач состоит из таких функций:

        1. task_parse_xml - эта функция нужна чтобы распарсить полученный XML файл и возвращает она список словарей.

        2. task_analyze_data - делает вычисления для составления llm prompt.

        3. task_generate_report - генерирует prompt запрос к LLM на генерацию отчета.

        4. task_save_result_to_db - сохраняет данные в БД.


    :param file: XML file

    :return: Celery Task ID
    """
    try:
        from src.celery.celery_worker import process_full_chain

        content = await file.read()
        task_chain = process_full_chain.apply_async(args=(content,))
        task_id = task_chain.id
    except Exception as e:
        my_logger.error(str(e))
        raise HTTPException(status_code=400, detail="Invalid XML or API connection")

    return {
        "result": "The report is being generated",
        "task_id": task_id,
    }


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Показывает состояние задач по id.

    :param task_id: id of the task

    :return: status of the task
    """
    result = AsyncResult(task_id)

    # Проходим по всем подзадачам
    for subtask in result.children or []:  # children может быть None
        if subtask.status == "FAILURE":
            return {
                "task_id": subtask.id,
                "status": subtask.state,
                "result": str(subtask.result),  # Представляем результат как строку
                "traceback": subtask.traceback,  # Добавляем traceback для отладки
            }

    # Если ошибок в подзадачах нет, возвращаем статус исходной задачи
    return {
        "task_id": task_id,
        "status": result.state,
        "result": str(result.result) if result.status != "PENDING" else None,
    }


@router.get(
    "/reports/",
    response_model=AIReportResponse,
)
@cache(expire=30)
async def get_ai_report(
    date_value: date = Query(..., description="Date example: '2024-01-01'"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Выдает сохраненный в БД llm отчет по дате.

    :param session: Подключение к Postgres.

    :param date_value: За какую дату хотите получить отчет.

    :return: Составленный AI отчет.
    """
    return await OrmQuery.get_report_by_date(session=session, date=date_value)


@router.get(
    "/sales-product/",
    response_model=List[ProductResponse],
)
@cache(expire=30)
async def get_sales_product(
    date_value: date = Query(..., description="Date example: '2024-01-01'"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
     Выдает сохраненные в БД данные из XML отчетов по дате.

    :param date_value: За какую дату хотите получить данные.

    :param session: Подключение к Postgres.

    :return: Список из product.
    """
    return await OrmQuery.get_product_by_date(session=session, date=date_value)
