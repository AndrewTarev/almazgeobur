from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: float
    category: str
    date: datetime
    model_config = ConfigDict(extra="ignore")


class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskID(BaseModel):
    ai_report: str = Field(
        title="Task id from Celery. You can get it for path '/parse-xml/'",
        max_length=50,
    )
    dict_data: list[dict[str, Any]] = Field(
        title="Task id from Celery. You can get it for path '/parse-xml/'",
        max_length=50,
    )
