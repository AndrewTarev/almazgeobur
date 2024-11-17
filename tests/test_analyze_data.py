import pytest

from src.core.utils.data_analyzer import analyze_data


def test_analyze_data_with_valid_sales_data():
    sales_data = [
        {
            "date": "2023-10-01",
            "name": "Product A",
            "category": "Category 1",
            "quantity": 10,
            "price": 5.0,
        },
        {
            "date": "2023-10-01",
            "name": "Product B",
            "category": "Category 2",
            "quantity": 20,
            "price": 10.0,
        },
        {
            "date": "2023-10-01",
            "name": "Product A",
            "category": "Category 1",
            "quantity": 5,
            "price": 5.0,
        },
    ]

    expected_date = "2023-10-01"
    expected_total_revenue = (10 * 5.0) + (20 * 10.0) + (5 * 5.0)  # 225.0
    expected_top_products_str = "Product B (20), Product A (15)"
    expected_categories_str = "Category 1: 15, Category 2: 20"

    result = analyze_data(sales_data)
    assert result[0] == expected_date
    assert result[1] == expected_total_revenue
    assert result[2] == expected_top_products_str
    assert result[3] == expected_categories_str


def test_analyze_data_with_empty_sales_data():
    with pytest.raises(ValueError, match="Data is empty."):
        analyze_data([])


def test_analyze_data_with_single_sale():
    sales_data = [
        {
            "date": "2023-10-01",
            "name": "Product A",
            "category": "Category 1",
            "quantity": 1,
            "price": 10.0,
        },
    ]

    expected_date = "2023-10-01"
    expected_total_revenue = 10.0
    expected_top_products_str = "Product A (1)"
    expected_categories_str = "Category 1: 1"

    result = analyze_data(sales_data)
    assert result[0] == expected_date
    assert result[1] == expected_total_revenue
    assert result[2] == expected_top_products_str
    assert result[3] == expected_categories_str
