from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Produits(BaseModel):
    id: str
    name: str
    composant: str 
    price: float
   

