import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field

from models.pharmacy import Pharmacy, ProductInPharmacy
from models.user import User





class Order(Document):
    user: Link [User]
    pharmacy: Link [Pharmacy]
    order_date: datetime = Field(default_factory=datetime.utcnow)
    productsInOrder: [List[Link[ProductInOrder]]]
    
    
    class Settings:
        name = "orders"
    
class ProductInOrder(Document):
    order: Link [Order]
    product: Link [ProductInPharmacy]
    quantity: int
    
    class Settings:
        name = "product_in_orders"
    
    
    
    
class ProductInOrderUpdate(BaseModel):
    quantity: Optional [int]
    
    

    