import asyncio
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base import Base
from src.core.db_helper import db_helper


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return f"<Product(product_name={self.name}, quantity={self.quantity}, price={self.price})>"


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
