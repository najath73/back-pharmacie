from itertools import product
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Query

from models.product import Product, UpdateProduct, AddProduct
from models.pharmacy import Pharmacy

router = APIRouter(prefix="/products", tags=["Products"])

#Get all products
@router.get("", status_code=200)
async def get_all_products(search: Optional[str] = Query(None, description="Search query to filter products by name")) -> List[Product]:
    if search:
        # Rechercher les produits correspondant au critère de recherche
        products = await Product.find({"name": {"$regex": search, "$options": "i"}}).to_list()
    else:
        # Retourner tous les produits si aucune recherche n'est spécifiée
        products = await Product.find_all().to_list()
    
    return products

#Post a product
@router.post("", status_code=201, response_model=dict)
async def post_a_product(payload: AddProduct):
    productToAdded= Product(name=payload.name, description=payload.description, img=payload.description, pharmacy=payload.pharmacy_id, quantity=payload.quantity, price= payload.price)
    product_added = await productToAdded.create()
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
       product_updated.description= payload.description
    if (payload.quantity):
       product_updated.quantity= payload.quantity
    if (payload.price):
       product_updated.price= payload.price
    if (payload.img):
       product_updated.img= payload.img
      
    await product_updated.save()
    return 
#delete product 
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
   product_deleted= await Product.get(product_id)
   await product_deleted.delete()
   return 

