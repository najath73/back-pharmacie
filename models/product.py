from typing import Optional
from beanie import Document
from pydantic import BaseModel




class Product(Document):
    name: str
    component: str 
    description: str
    class Settings:
        name = "produits"
        
class UpdateProduct(BaseModel): 
    name: Optional [str]
    component: Optional [str] 
    description: Optional[str]
        

