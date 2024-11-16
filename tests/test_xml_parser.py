from unittest.mock import MagicMock
from defusedxml.ElementTree import ParseError

import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from src.core.utils.xml_parser import parse_xml


def test_parse_xml_valid_data():
    xml_content = """
    <sales_data date="2024-01-01">
        <products>
            <product>
                <id>1</id>
                <name>Product A</name>
                <quantity>100</quantity>
                <price>1500.00</price>
                <category>Electronics</category>
            </product>
        </products>
    </sales_data>
    """
    result = parse_xml(xml_content)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["name"] == "Product A"
    assert result[0]["quantity"] == 100
    assert result[0]["price"] == 1500.00
    assert result[0]["category"] == "Electronics"


def test_parse_xml_invalid_xml():
    xml_content = """
    <sales_data date="2024-01-01">
        <products>
            <product>
                <id>1</id>
                <name>Product A<name> <!-- Открывающий и закрывающий теги не совпадают -->
                <quantity>100</quantity>
    """
    with pytest.raises(HTTPException) as exc_info:
        parse_xml(xml_content)

    assert exc_info.value.detail == "Invalid XML format"


def test_parse_xml_invalid_date_format():
    xml_content = """
    <sales_data date="01-01-2024">
        <products>
            <product>
                <id>1</id>
                <name>Product A</name>
                <quantity>100</quantity>
                <price>1500.00</price>
                <category>Electronics</category>
            </product>
        </products>
    </sales_data>
    """
    with pytest.raises(HTTPException) as exc_info:
        parse_xml(xml_content)
    assert exc_info.value.detail == "Invalid date format in XML data"


def test_parse_xml_no_products():
    xml_content = """
    <sales_data date="2024-01-01">
    </sales_data>
    """
    with pytest.raises(HTTPException) as exc_info:
        parse_xml(xml_content)

    assert exc_info.value.detail == "No <products> found in XML"


def test_parse_xml_no_date_attribute():
    xml_content = """
    <sales_data>
        <products>
            <product>
                <id>1</id>
                <name>Product A</name>
                <quantity>100</quantity>
                <price>1500.00</price>
                <category>Electronics</category>
            </product>
        </products>
    </sales_data>
    """
    result = parse_xml(xml_content)
    assert isinstance(result, list)
    assert len(result) == 1
