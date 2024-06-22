from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Pharmaie(BaseModel):
    id: str
    name: str
    adresse: str 
    numéro: float
   

