from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from enum import Enum
from models.pharmacy import Pharmacy
from models.product import Product
from models.user import User


class StatusOrder(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class ProductInOrder(BaseModel):
    product: Link[Product]
    unitPrice: float
    quantity: int
    

class Order(Document):
    user: Link [User]
    pharmacy: Link[Pharmacy]
    productsInOrder: List[ProductInOrder]
    date: datetime = datetime.now()
    status: StatusOrder  = Field(default=StatusOrder.PENDING)
    
    
    class Settings:
        name = "orders"

class OrderUpdate(BaseModel):
    status: StatusOrder

class ProductInOrderPost(BaseModel): 
    product: str
    quantity: int
class PostOrder(BaseModel):
    pharmacy_id: str
    producstInOrder: List[ProductInOrderPost]


