from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel

from models.pharmacy import Pharmacy, ProductInPharmacy
from models.user import User





class Order(Document):
    user: Link [User]
    pharmacy: Link [Pharmacy]
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
    
    

    