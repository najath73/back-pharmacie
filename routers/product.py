from typing import List
from fastapi import APIRouter

from models.product import Product, UpdateProduct
from models.pharmacy import Pharmacy

router = APIRouter(prefix="/product", tags=["Products"])

#Get all product
@router.get("/pharmacies/{pharmacy_id}/products", status_code=200,response_model=list)
async def get_all_products_in_pharmacy(pharmacy_id: str) :
   pharmacy= await Pharmacy.get(pharmacy_id)
   products= await pharmacy.Product.find_all().to_list()
   return products

#Post a product 
@router.post("/pharmacies/{pharmacy_id}/products", status_code=201, response_model=dict)
async def post_product_to_pharmacy(pharmacy_id: str, payload: Product):
   pharmacy= Pharmacy.get(pharmacy_id)
   product_created = await pharmacy.payload.create() # Or payload.insert()
   return {"message": "Product added successfully", "id": product_created.id}

#Get product by id
@router.get("/pharmacies/{pharmacy_id}/products/{product_id}", status_code=200)
async def get_product_by_id_in_pharmacy(pharmacy_id: str, product_id: str) -> Product :
   pharmacy= Pharmacy.get(pharmacy_id)
   product= await pharmacy.Product.get(product_id)
   return product

#update product 
@router.patch("/pharmacies/{pharmacy_id}/products/{product_id}", status_code=200)
async def update_product_in_pharmacie(pharmacy_id: str, product_id: str , payload: UpdateProduct):
   pharmacy= await Pharmacy.get(pharmacy_id)
   product= await pharmacy.Product.get(product_id)
   if (payload.name):
      product.name=payload.name

   if (payload.component):
      product.component=payload.component
     
   if (payload.description):
      product.description=payload.description
      
   await product.save()
   return 

#delete product 
@router.delete("/pharmacies/{pharmacy_id}/products/{product_id}")
async def delete_product_in_pharmacy(pharmacy_id,product_id: str):
   pharmacy= await Pharmacy.get(pharmacy_id)
   product= await pharmacy.Product.get(product_id)
   await product.delete()
   return {"message":"Produit supprimer avec succes"}