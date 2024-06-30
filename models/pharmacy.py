from pydantic import BaseModel
from beanie import Document, Link
from models.product import Product
from typing import Optional



class Localisation(BaseModel):
    longitude: float
    latitude: float
 




class Pharmacy(Document):
    name: str
    adress: str 
    phone: float
    localisation: Localisation
   
    class Settings:
        name = "pharmacies"
   
class UpdatePharmacy(BaseModel):
    name: Optional [str]
    adress: Optional [str]
    phone: Optional [str]
    Localisation: Optional [str]
    products: Optional [str]
    
class ProductsInPharmacy(Document):
    product: Link[Product]
    price: float
    quantity: int
    pharmacy: Link[Pharmacy]  

class ProductInPharmacyAdd(BaseModel):
    price: float
    quantity: int

class ProductInPharmacypdate(BaseModel):
    price:float
    quantity: int

    




