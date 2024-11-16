import asyncio
from datetime import datetime
from typing import List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.db_helper import db_helper


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("llm_report.id"))
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    llm_report: Mapped["LLMreport"] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product(product_name={self.name}, quantity={self.quantity}, price={self.price})>"


class LLMreport(Base):
    __tablename__ = "llm_report"
    id: Mapped[int] = mapped_column(primary_key=True)
    ai_report: Mapped[str] = mapped_column()

    product: Mapped[List["Product"]] = relationship(back_populates="llm_report")

    def __repr__(self):
        return f"<LLMreport(ai_report={self.ai_report}>"


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
