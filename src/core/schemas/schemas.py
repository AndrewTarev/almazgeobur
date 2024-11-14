from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
