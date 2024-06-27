from typing import List
from fastapi import APIRouter

from models.pharmacy import Pharmacy, UpdatePharmacy
from models.product import Product, UpdateProduct

router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

#Get all pharmacy
@router.get("", status_code=200)
async def get_all_pharmacies() -> List [Pharmacy]:
    pharmacy= await Pharmacy.find_all().to_list()
    return pharmacy

#Post a pharmacy
@router.post("", status_code=201, response_model=dict)
async def post_a_pharmacy(payload: Pharmacy):
    pharmacy_added= await payload.create()
    return {"message": "Pharmacy added successfully", "id":pharmacy_added.id}

#Get pharmacy by id
@router.get("/{pharmacy_id}",status_code=200)
async def get_pharmacy_by_id(pharmacy_id: str) ->Pharmacy:
    pharmacy= await Pharmacy.get(pharmacy_id)
    return pharmacy

#Update pharmacy
@router.patch("/{pharmacy_id}",status_code=204)
async def update_pharmacy(pharmacy_id: str , payload: UpdatePharmacy):
   pharmacy_updated= await Pharmacy.get(pharmacy_id)
   if (payload.name):
       pharmacy_updated.name= payload.name
       
       
   if (payload.adress):
       pharmacy_updated.adress= payload.adress
       
   if (payload.phone):
       pharmacy_updated.phone= payload.phone
       
   if (payload.localisation):
       pharmacy_updated.localisation= payload.localisation
    
   if (payload.products):
       pharmacy_updated.products = payload.products
       

      
   await pharmacy_updated.save()
   return 

#delete pharmacy 
@router.delete("/{pharmacy_id}", status_code=204)
async def delete_pharmacy(pharmacy_id: str):
   pharmacy_deleted= await Pharmacy.get(pharmacy_id)
   await pharmacy_deleted.delete()
   return {"message":"Pharmacy deleted successfully"}
    
    
#Get all product in a pharmacy
@router.get("/{pharmacy_id}/products", status_code=200)
async def get_all_products_in_pharmacy(pharmacy_id: str) -> List [Product] :
   pharmacy= await Pharmacy.get(pharmacy_id)
   products= await pharmacy.products.find_all().to_list()
   return products

#Post a product in a pharmacy
@router.post("/{pharmacy_id}/products", status_code=201, response_model=dict)
async def post_product_to_pharmacy(pharmacy_id: str, payload: Product):
   pharmacy= Pharmacy.get(pharmacy_id)
   product_created = await pharmacy.payload.create() # Or payload.insert()
   return {"message": "Product added successfully", "id": product_created.id}

#Get product by id a pharmacy
@router.get("/{pharmacy_id}/products/{product_id}", status_code=200)
async def get_product_by_id_in_pharmacy(pharmacy_id: str, product_id: str) -> Product :
   pharmacy= Pharmacy.get(pharmacy_id)
   product= await pharmacy.Product.get(product_id)
   return product

#update product in a pharmacy
@router.patch("/{pharmacy_id}/products/{product_id}", status_code=200)
async def update_product_in_pharmacie(pharmacy_id: str, product_id: str , payload: UpdateProduct):
   pharmacy= await Pharmacy.get(pharmacy_id)
   product= await pharmacy.products.get(product_id)
   if (payload.name):
      product.name=payload.name

   if (payload.component):
      product.component=payload.component
     
   if (payload.description):
      product.description=payload.description
      
   await product.save()
   return 

#delete product in a pharmacy
@router.delete("/{pharmacy_id}/products/{product_id}")
async def delete_product_in_pharmacy(pharmacy_id,product_id: str):
   pharmacy= await Pharmacy.get(pharmacy_id)
   product= await pharmacy.Product.get(product_id)
   await product.delete()
   return {"message":"Produit supprimer avec succes"}
    
      
    
    
      
    
        