from typing import Optional
from beanie import Document, Link
from pydantic import BaseModel
from models.pharmacy import Pharmacy



class Product(Document):
    name: str
    description: str
    img: str
    quantity: float
    price: float
    pharmacy: Link[Pharmacy]
    class Settings:
        name = "products"
        
class UpdateProduct(BaseModel): 
    name: Optional [str] = None
    description: Optional[str] = None
    img: Optional[str] = None
    quantity: Optional[float]= None
    price: Optional[float]= None
    pharmacy_id: Optional[str] = None


class AddProduct(BaseModel):
    name: str
    description: str = "Description"
    img: Optional[str]
    quantity: float
    price: float
    pharmacy_id: str