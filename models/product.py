from typing import Optional
from beanie import Document
from pydantic import BaseModel




class Product(Document):
    name: str
    description: str
    class Settings:
        name = "products"
        
class UpdateProduct(BaseModel): 
    name: Optional [str]
    description: Optional[str]
        

