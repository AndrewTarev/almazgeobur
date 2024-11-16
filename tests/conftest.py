from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.core import Base
from src.core.config import settings
from src.core.db_helper import db_helper
from src.main import app

# test_db = settings.test_db.url
# engine = create_async_engine(test_db, echo=True, poolclass=NullPool)
# async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def override_get_db() -> AsyncGenerator:
#     async with async_session() as session:
#         yield session
#
#
# app.dependency_overrides[db_helper.session_getter] = override_get_db
#

# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest_asyncio.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as async_client:
#         yield async_client
