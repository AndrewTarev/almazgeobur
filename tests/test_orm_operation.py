from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from src.api.v1.cruds.product_crud import OrmQuery
from src.core import LLMreport, Product
from src.core.schemas.schemas import ProductBase


@pytest.mark.asyncio
async def test_create_new_products_and_report() -> None:
    mock_data = [
        ProductBase(
            name="Product1",
            price=10.0,
            quantity=2,
            category="A",
            date=datetime.now(),
        ),
        ProductBase(
            name="Product2",
            price=20.0,
            quantity=3,
            category="B",
            date=datetime.now(),
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
async def test_get_report_by_date_success(mocker: MagicMock) -> None:
    # Создаем фиктивные объекты
    fake_session = AsyncMock()
    fake_results = MagicMock()
    fake_report = MagicMock(spec=LLMreport)

    # Устанавливаем, что будет возвращено при выполнении execute
    fake_session.execute.return_value = fake_results

    # Настраиваем возврат scalsars().first() чтобы это возвращало наш fake_report
    fake_results.scalars.return_value.first.return_value = fake_report

    # Дата, которая будет использоваться в тесте
    test_date = datetime(2023, 10, 5)

    # Вызов функции
    report = await OrmQuery.get_report_by_date(fake_session, test_date)

    # Проверка результатов
    fake_session.execute.assert_called_once_with(
        mocker.ANY
    )  # Проверяем, что execute вызван
    assert report == fake_report


@pytest.mark.asyncio
async def test_get_report_by_date_not_found() -> None:
    # Создаем фиктивные объекты
    fake_session = AsyncMock()
    fake_results = MagicMock()

    # Устанавливаем, что будет возвращено при выполнении execute
    fake_session.execute.return_value = fake_results
    fake_results.scalars.return_value.first.return_value = None  # Нет данных

    # Дата, которая будет использоваться в тесте
    test_date = datetime(2023, 10, 5)

    # Вызов функции должен вызвать исключение HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await OrmQuery.get_report_by_date(fake_session, test_date)

    # Проверка, что вызвалось правильное исключение
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "No reports found for the given date"


@pytest.mark.asyncio
async def test_get_product_by_date_success(mocker: MagicMock) -> None:
    # Создаем фиктивные объекты
    fake_session = AsyncMock()
    fake_results = MagicMock()
    fake_product_1 = MagicMock(spec=Product)
    fake_product_2 = MagicMock(spec=Product)

    # Устанавливаем, что будет возвращено при выполнении execute
    fake_session.execute.return_value = fake_results

    # Настраиваем возврат scalars().all() чтобы вернуть список продуктов
    fake_results.scalars.return_value.all.return_value = [
        fake_product_1,
        fake_product_2,
    ]

    # Дата, которая будет использоваться в тесте
    test_date = datetime(2023, 10, 5)

    # Вызов функции
    products = await OrmQuery.get_product_by_date(fake_session, test_date)

    # Проверка результатов
    fake_session.execute.assert_called_once_with(
        mocker.ANY
    )  # Проверить, что execute вызван
    assert products == [fake_product_1, fake_product_2]


@pytest.mark.asyncio
async def test_get_product_by_date_not_found() -> None:
    # Создаем фиктивные объекты
    fake_session = AsyncMock()
    fake_results = MagicMock()

    # Устанавливаем, что будет возвращено при выполнении execute
    fake_session.execute.return_value = fake_results

    # Настраиваем scalars().all() чтобы вернуть пустой список
    fake_results.scalars.return_value.all.return_value = []

    # Дата, которая будет использоваться в тесте
    test_date = datetime(2023, 10, 5)

    # Вызов функции должен вызвать исключение HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await OrmQuery.get_product_by_date(fake_session, test_date)

    # Проверка, что вызвалось правильное исключение
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "No products found for the given date"
