from typing import List
from fastapi import APIRouter

from models.product import Product, UpdateProduct

router = APIRouter(prefix="/product", tags=["Products"])

#Get all product
@router.get("", status_code=200,response_model=list)
async def get_all_products() :
   products= await Product.find_all().to_list()
   return products

#Post a product 
@router.post("", status_code=201, response_model=dict)
async def post_product(payload: Product):
   product_created = await payload.create() # Or payload.insert()
   return {"message": "Product added successfully", "id": product_created.id}

#Get product by id
@router.get("/{product_id}", status_code=200)
async def get_product_by_id(product_id: str) -> Product :
   product= await Product.get(product_id)
   return product

#update product by id
@router.patch("/{product_id}")
async def update_product_by_id(product_id: str , payload: UpdateProduct):
   product= await Product.get(product_id)
   if (payload.name):
      product.name=payload.name

   if (payload.component):
      product.component=payload.component
     
   if (payload.description):
      product.description=payload.description
      
   await product.save()
   return product
#delete product by id
@router.delete("/{product_id}")
async def delete_product_by_id(product_id: str):
   product= await Product.get(product_id)
   await product.delete()
   return ("Produit supprimer avec succes")