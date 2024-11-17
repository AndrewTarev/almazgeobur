import asyncio

from celery import chain

from src.api.v1.cruds.product_crud import OrmQuery
from src.celery.celery_app import celery_app
from src.core.utils.data_analyzer import analyze_data
from src.core.utils.logging_config import my_logger
from src.core.utils.xml_parser import parse_xml
from src.core.utils.sales_data_prompt import generate_report_content


@celery_app.task
def task_parse_xml(xml_text):
    """
    Запускает функцию которая парсит XML контент.
    :param xml_text: XML content
    :return: List[Dict[str, Any]]
    """
    return parse_xml(xml_text)


@celery_app.task
def task_analyze_data(prod_list):
    """
    Принимает распаршенный контент и делает вычисления для составления prompt запрос к llm.
    :param prod_list: List[Dict[str, Any]] распаршенный контент
    :return: tuple(date, total_revenue, top_products_str, categories_str),
        prod_list - передает дальше по цепочке распаршеный XML content
    """
    result: tuple = analyze_data(prod_list)
    return result, prod_list


@celery_app.task
def task_generate_report(analyze_report: tuple):
    """
    Генерирует prompt и отправляет запрос к LLM на генерацию отчета.
    """
    dict_data_result = analyze_report[1]  # Распаршенный XML контент
    analyze_report = analyze_report[0]

    date, total_revenue, top_products, categories = analyze_report
    ai_report_result = generate_report_content(
        date=date,
        total_revenue=total_revenue,
        top_products=top_products,
        categories=categories,
    )
    return ai_report_result, dict_data_result


@celery_app.task
def task_save_result_to_db(data: tuple):
    """Сохраняет данные в БД"""
    ai_report, data_dict = data
    asyncio.run(
        OrmQuery.create_new_products_and_report(
            ai_report=ai_report,
            data=data_dict,
        )
    )


@celery_app.task
def process_full_chain(content):
    my_logger.debug("Starting process_full_chain")
    report_chain = chain(
        task_parse_xml.s(content),
        task_analyze_data.s(),
        task_generate_report.s(),
        task_save_result_to_db.s(),
    )
    result = report_chain.apply_async()
    return {"result": "Success"}
