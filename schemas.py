from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import enum

class PaymentMethodEnum(str, enum.Enum):
    cash = "cash"
    card = "card"
    mobile = "mobile"

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemRead(SaleItemBase):
    id: int
    price: float
    product: ProductRead
    class Config:
        orm_mode = True

class SaleCreate(BaseModel):
    items: List[SaleItemBase]
    payment_method: PaymentMethodEnum

class SaleRead(BaseModel):
    id: int
    created_at: datetime
    total_amount: float
    payment_method: PaymentMethodEnum
    items: List[SaleItemRead]
    class Config:
        orm_mode = True 