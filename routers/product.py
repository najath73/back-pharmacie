from itertools import product
from typing import List
from bson import ObjectId
from fastapi import APIRouter

from models.product import Product, UpdateProduct
from models.pharmacy import Pharmacy

router = APIRouter(prefix="/products", tags=["Products"])

#Get all products
@router.get("", status_code=200)
async def get_all_products() -> List [Product]:
    product= await Product.find_all().to_list()
    return product

#Post a product
@router.post("", status_code=201, response_model=dict)
async def post_a_product(payload: Product):
    product_added= await payload.create()
    return {"message": "Product added successfully", "id": str(product_added.id)}

#Get product by idfetch_links=True,
@router.get("/{product_id}",status_code=200)
async def get_product_by_id(product_id: str) ->Product:
    product= await Product.get(product_id)
    return product

#Update product
@router.patch("/{product_id}",status_code=204)
async def update_product(product_id: str , payload:UpdateProduct ):
   product_updated= await Product.get(product_id)
   if (payload.name):
       product_updated.name= payload.name
       
       
   if (payload.description):
       product_updated= payload.description
       

       

      
   await product_updated.save()
   return 

#delete product 
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
   product_deleted= await Product.get(product_id)
   await product_deleted.delete()
   return 

