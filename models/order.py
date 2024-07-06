from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel

from models.pharmacy import Pharmacy, ProductInPharmacy
from models.user import User


class ProductInOrder(BaseModel):
    products: Link [List[ProductInPharmacy]]
    pharmacy: Link [Pharmacy]
    

class OrderInPharmacy(Document):
    user: Link [User]
    productInOrder: ProductInOrder
    
class OrderUpdate(BaseModel):
    user: Link [User]
    productInOrder: Optional [List[ProductInOrder]]
    
    

    