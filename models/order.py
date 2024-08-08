from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from enum import Enum
from models.pharmacy import Pharmacy, ProductInPharmacy
from models.user import User


class StatusOrder(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class ProductInOrder(Document):
    productInPharmcy: Link [ProductInPharmacy]
    quantity: int
    
    class Settings:
        name = "product_in_orders"
    

class Order(Document):
    user: Link [User]
    productsInOrder: List[Link[ProductInOrder]]
    status: StatusOrder  = Field(default=StatusOrder.PENDING)
    
    
    class Settings:
        name = "orders"

class OrderUpdate(BaseModel):
    status: StatusOrder
    
class ProductInOrderPost(BaseModel):
    pharmacy_id: str
    product_id: str
    quantity: int

class PostOrder(BaseModel):
    producstInOrder: List[ProductInOrderPost]


