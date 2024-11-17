import pytest
import defusedxml.ElementTree as ET

from src.core.utils.xml_parser import parse_xml


def test_parse_xml_successful():
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
            <product>
                <id>2</id>
                <name>Product B</name>
                <quantity>50</quantity>
                <price>500.00</price>
                <category>Home</category>
            </product>
        </products>
    </sales_data>
    """

    expected_sales_data = [
        {
            "name": "Product A",
            "quantity": 100,
            "price": 1500.0,
            "category": "Electronics",
            "date": "2024-01-01",
        },
        {
            "name": "Product B",
            "quantity": 50,
            "price": 500.0,
            "category": "Home",
            "date": "2024-01-01",
        },
    ]

    result = parse_xml(xml_content)
    assert result == expected_sales_data


def test_parse_xml_no_products():
    xml_content = """
    <sales_data date="2024-01-01">
    </sales_data>
    """

    with pytest.raises(AttributeError, match="No <products> found in XML"):
        parse_xml(xml_content)


def test_parse_xml_missing_field():
    xml_content = """
    <sales_data date="2024-01-01">
        <products>
            <product>
                <id>1</id>
                <name>Product A</name>
                <price>1500.00</price>
                <category>Electronics</category>
            </product>
        </products>
    </sales_data>
    """

    with pytest.raises(AttributeError):
        parse_xml(xml_content)


def test_parse_xml_invalid_data_type():
    xml_content = """
    <sales_data date="2024-01-01">
        <products>
            <product>
                <id>1</id>
                <name>Product A</name>
                <quantity>invalid_number</quantity> <!-- Invalid quantity -->
                <price>1500.00</price>
                <category>Electronics</category>
            </product>
        </products>
    </sales_data>
    """

    with pytest.raises(ValueError):
        parse_xml(xml_content)


def test_parse_xml_invalid_xml():
    xml_content = "<sales_data><products><product></products>"

    with pytest.raises(ET.ParseError):
        parse_xml(xml_content)
