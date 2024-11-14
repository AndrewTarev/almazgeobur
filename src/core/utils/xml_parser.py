from datetime import datetime
from typing import Dict, Any, List

import defusedxml.ElementTree as ET
from fastapi import HTTPException

from src.core.schemas.schemas import ProductBase
from src.core.utils.logging_config import my_logger


def parse_xml(xml_content) -> List[Dict[str, Any]]:
    """
    Parse XML content and return a list of dictionaries.
    :param xml_content: xml content to be parsed.
    :return: parsed XML content
    """
    try:
        root = ET.fromstring(xml_content)
        sales_data = []

        # Извлечение даты из атрибута корневого элемента
        date = root.attrib.get("date")

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        for product in root.find("products"):
            sales_data.append(
                {
                    "id": product.find("id").text,
                    "name": product.find("name").text,
                    "quantity": int(product.find("quantity").text),
                    "price": float(product.find("price").text),
                    "category": product.find("category").text,
                    "date": date,
                }
            )
    except ET.ParseError:
        my_logger.error("Invalid XML data")
        raise HTTPException(status_code=400, detail="Invalid XML data")
    except Exception as e:
        my_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))

    my_logger.info("XML parsed successfully")
    return sales_data
