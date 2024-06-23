from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field



class Product(Document):
    name: str
    description: Optional[str]

    class Settings:
        name = "products"

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None