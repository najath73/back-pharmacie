from typing import List
from fastapi import APIRouter

from models.product import Product

router = APIRouter(prefix="/product", tags=["Products"])

@router.get("", status_code=200)
async def get_all_products() :
   products= await Product.find_all().to_list()
   return products

@router.post("", status_code=201, response_model=dict)
async def post_product(payload: Product):
   product_created = await payload.create() # Or payload.insert()
   return {"message": "Product added successfully", "id": product_created.id}