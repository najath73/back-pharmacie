from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from models.product import Product



class Localisation(BaseModel):
    longitude: float
    latitude: float

class Pharmacy(Document):
    name: str
    address: str
    phone: str
    localisation: Localisation

    class Settings:
        # The name of the collection to store these objects.
        name = "pharmacies"
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "name": "Pharmacie",
                "address": "2 carrefour du matin",
                "phone": "+224624236756",
                "localisation": {
                    "longitude": 120.23,
                    "latitude": -134.7
                }
            }
        }
        

class ProductInPharmacy(Document):
    product: Link[Product]
    pharmacy: Link[Pharmacy]
    price: float
    quantity: int


class PharmacyUpdated(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    localisation: Optional[Localisation]


class ProductInPharmacyAdd(BaseModel):
    price: float
    quantity: int

class ProductInPharmacyUpdate(BaseModel):
    price: Optional[float]
    quantity: Optional[int]
