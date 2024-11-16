import defusedxml.ElementTree as ET
from src.core.utils.logging_config import my_logger

from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException


def parse_xml(xml_content) -> List[Dict[str, Any]]:
    """
    Парсит XML контент.
    :param xml_content: xml content to be parsed.
    :return: parsed XML content
    """
    my_logger.debug("Task parse_xml started")

    sales_data = []

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        my_logger.error(str(e))
        raise HTTPException(status_code=400, detail="Invalid XML format")

    # Извлечение даты из атрибута корневого элемента
    date = root.attrib.get("date")

    products = root.find("products")
    if products is None:
        my_logger.error("No <products> found in XML")

    for product in products:
        try:
            sales_data.append(
                {
                    "id": product.find("id").text,
                    "name": product.find("name").text,
                    "quantity": int(product.find("quantity").text),
                    "price": float(product.find("price").text),
                    "category": product.find("category").text,
                    "date": str(date),
                }
            )
        except AttributeError as ae:
            my_logger.error(f"Missing required product field: {ae}")

        except ValueError as ve:
            my_logger.error(f"Invalid data type for product field: {ve}")

    my_logger.info("XML parsed successfully")
    return sales_data
