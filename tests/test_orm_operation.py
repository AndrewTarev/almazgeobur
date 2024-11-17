import datetime
from unittest.mock import patch, AsyncMock

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models.shop_model import Product, LLMreport
from src.core.schemas.schemas import ProductBase
from src.api.v1.cruds.product_crud import OrmQuery


@pytest.mark.asyncio
async def test_create_new_products_and_report():
    mock_data = [
        ProductBase(
            name="Product1",
            price=10.0,
            quantity=2,
            category="A",
            date=datetime.datetime.now(),
        ),
        ProductBase(
            name="Product2",
            price=20.0,
            quantity=3,
            category="B",
            date=datetime.datetime.now(),
        ),
    ]

    with patch("src.core.db_helper.db_helper.session_factory") as mock_session_factory:
        mock_session = AsyncMock()
        mock_session_factory.return_value.__aenter__.return_value = mock_session

        result = await OrmQuery.create_new_products_and_report(
            "Sample Report", mock_data
        )

        assert len(result) == len(mock_data)
        assert mock_session.add.call_count == 1  # For report
        assert mock_session.add_all.call_count == 1  # For products
        assert mock_session.commit.call_count == 1  # Commit operation


@pytest.mark.asyncio
async def test_get_report_by_date_success():
    # Создаем моковую сессию
    session_mock = AsyncMock()
    fake_report = LLMreport(ai_report="Test")
    # Мокаем результат выполнения запроса
    session_mock.execute.return_value.scalars.return_value.first.return_value = (
        fake_report
    )

    # Вызываем метод
    result = await OrmQuery.get_report_by_date(session_mock, datetime.date.today())

    # Проверяем результат
    assert result == fake_report


@pytest.mark.asyncio
async def test_get_report_by_date_not_found():
    # Создаем моковую сессию
    session_mock = AsyncMock()
    # Мокаем отсутствие результата
    session_mock.execute.return_value.scalars.return_value.first.return_value = None

    # Проверяем, что выбрасывается HTTPException
    with pytest.raises(HTTPException):
        await OrmQuery.get_report_by_date(session_mock, datetime.date.today())


@pytest.mark.asyncio
async def test_get_report_by_date_not_found():
    date = datetime.datetime.now()

    with patch.object(OrmQuery, "_execute_select", return_value=None) as mock_select:
        async with AsyncMock() as mock_session:
            with pytest.raises(HTTPException) as exc_info:
                await OrmQuery.get_report_by_date(mock_session, date)
            assert exc_info.value.status_code == 404
            mock_select.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_by_date_found():
    date = datetime.datetime.now()
    mock_product_list = [
        Product(name="Product1", price=10.0, quantity=2, category="A", date=date),
        Product(name="Product2", price=20.0, quantity=3, category="B", date=date),
    ]

    with patch.object(
        OrmQuery, "_execute_select", return_value=mock_product_list
    ) as mock_select:
        async with AsyncMock() as mock_session:
            result = await OrmQuery.get_product_by_date(mock_session, date)
            assert result == mock_product_list
            mock_select.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_by_date_not_found():
    date = datetime.datetime.now()

    with patch.object(OrmQuery, return_value=[]) as mock_select:
        async with AsyncMock() as mock_session:
            with pytest.raises(HTTPException) as exc_info:
                await OrmQuery.get_product_by_date(mock_session, date)
            assert exc_info.value.status_code == 404
            mock_select.assert_called_once()
