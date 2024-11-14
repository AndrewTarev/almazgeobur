from src.celery.celery_app import celery_app
from src.core.utils.data_analyzer import analyze_data
from src.core.utils.logging_config import my_logger
from src.prompt.sales_data_prompt import GenerateReport


@celery_app.task
def task_analyze_data(prod_list):
    my_logger.info("Analyzing data")
    return analyze_data(prod_list)


@celery_app.task
def task_generate_and_save_report(
    date: str, total_revenue: float, top_products: list, categories: list
):
    """
    Celery task for generating and saving the report.
    """
    my_logger.info(f"Task initiated for date: {date}")
    try:
        result = GenerateReport(date, total_revenue, top_products, categories)
        my_logger.info(f"Report generated successfully: {result}")
        return result()
    except Exception as e:
        my_logger.error(f"Error generating report: {str(e)}")
        raise e
