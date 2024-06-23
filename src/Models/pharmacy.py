from pydantic import BaseModel
from beanie import Document, Link
from Models.products import Product
from typing import Optional



class Localisation(BaseModel):
    longitude: float
    latitude: float
    
class ProductInPharmacie(BaseModel):
    produit: Link[Product]
    price: float


class Pharmacy(Document):
    name: str
    adress: str 
    phone: float
    localisation: Localisation
    products: list[ProductInPharmacie]= []
    
    class Settings:
        name = "pharmacies"
   
class UpdatePharmacie(BaseModel):
    name: Optional [str]
    adress: Optional [str]
    phone: Optional [str]
    Localisation: Optional [str]
    products: Optional [str]




