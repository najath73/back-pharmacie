from pydantic import BaseModel
from beanie import Document, Link
from models.product import Product
from typing import Optional



class Localisation(BaseModel):
    longitude: float
    latitude: float
    
class ProductsInPharmacy(BaseModel):
    produit: Link[Product]
    price: float


class Pharmacy(Document):
    name: str
    adress: str 
    phone: float
    localisation: Localisation
    products: list[ProductsInPharmacy]= []
    
    class Settings:
        name = "pharmacies"
   
class UpdatePharmacy(BaseModel):
    name: Optional [str]
    adress: Optional [str]
    phone: Optional [str]
    Localisation: Optional [str]
    products: Optional [str]




