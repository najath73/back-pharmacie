from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from models.product import Product

        
class ProductInPharmacy(BaseModel):
    product: Link[Product]
    price: float
    quantity: int


class Localisation(BaseModel):
    longitude: float
    latitude: float

class Pharmacy(Document):
    name: str
    address: str
    phone: str
    localisation: Localisation
    products: List[ProductInPharmacy] = []

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
                },
                "products": [
                    {
                        "product": {
                            'id': "2345678UHT5456789",
                            "collection": "product"
                        },
                        "price": 12.8,
                        "quantity": 25

                    },
                    {
                        "product": {
                            'id': "2345678UHTghjk456789",
                            "collection": "product"
                        },
                        "price": 14.7

                    }
                ]
            }
        }
        

class PharmacyUpdated(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    localisation: Optional[Localisation]


