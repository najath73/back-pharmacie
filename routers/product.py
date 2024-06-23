from typing import List
from fastapi import APIRouter

from models.product import Product, ProductUpdate




router = APIRouter(prefix="/produts", tags=["Products"])

#Get all products
@router.get("", status_code=200)
async def get_products() -> List[Product]:
   products = await Product.find_all().to_list()
   return products


#post a product
@router.post("", status_code=201)
async def post_product(product: Product) :
   new_product = await product.create()
   return  {"message": "categorie ajouté avec succès"}


#get by id a product
@router.get("/{product_id}", status_code=200)
async def get_product_by_id(product_id: str)-> Product:
   product = await Product.get(product_id) 
   return product


#update product by id
@router.patch("/{product_id}", status_code=204)
async def update_product(product_id: str, payload: ProductUpdate):
   product = await Product.get(product_id)
   if(payload.name):
      product.name = payload.name
      await product.save()
   if(payload.description):
      product.description = payload.description
      await product.save()
   return 

#delete product by id
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
   product = await Product.get(product_id)
   return 