from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, status, HTTPException

from src.core.utils.logging_config import my_logger


router = APIRouter()


@router.post(
    "/parse-xml/",
    status_code=status.HTTP_201_CREATED,
)
async def parse_xml_endpoint(
    file: UploadFile,
):
    """
    Этот эндпоинт принимает XML файл, создает цепочку фоновых задач в Celery.
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
    result = AsyncResult(task_id)
    if result.state == "FAILURE":
        raise HTTPException(status_code=400, detail=str(result.info))
    return {"task_id": task_id, "status": result.state, "result": result.result}
