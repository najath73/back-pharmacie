from typing import Optional
from beanie import Document, Link
from pydantic import BaseModel
from models.pharmacy import Pharmacy

class Category(Document):
    name: str
    description: str
class Product(Document):
    name: str
    description: str
    img: str
    stock: float
    price: float
    pharmacy: Link[Pharmacy]
    prescription: bool = False
    category: Link[Category]
    class Settings:
        name = "products"
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "name": "Product",
                "description": "This is a product",
                "img": "https://example.com/image.jpg",
                "quantity": 10,
                "price": 10.0,
                "pharmacy": "13HJJER8HH!888U",
                "prescription": False,
                "category": "13HJJER8HH!888U"
            }
        }
        
class UpdateProduct(BaseModel): 
    name: Optional [str] = None
    description: Optional[str] = None
    img: Optional[str] = None
    stock: Optional[float]= None
    price: Optional[float]= None
    pharmacy_id: Optional[str] = None
    prescription: Optional[bool] = False
    category_id: Optional[str] = None

class AddProduct(BaseModel):
    name: str
    description: str = "Description"
    img: Optional[str] = None
    stock: float
    price: float
    pharmacy_id: str
    prescription: Optional[bool] = False
    category_id: Optional[str] = None