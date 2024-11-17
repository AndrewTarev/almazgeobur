from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: float
    category: str
    date: datetime
    model_config = ConfigDict(extra="ignore")


class AIReportResponse(BaseModel):
    id: int
    ai_report: str


class ProductResponse(ProductBase):
    id: int


class ParseEndpointResponse(BaseModel):
    result: str
    task_id: str
