from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException

from models.pharmacy import Pharmacy, ProductInPharmacyAdd, PharmacyUpdated, ProductInPharmacy,ProductInPharmacyUpdate
from models.product import Product

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
    return {"message": "Pharmacy added successfully", "id": str(pharmacy_added.id)}

#Get pharmacy by id
@router.get("/{pharmacy_id}",status_code=200)
async def get_pharmacy_by_id(pharmacy_id: str) ->Pharmacy:
    pharmacy= await Pharmacy.get(pharmacy_id)
    return pharmacy

#Update pharmacy
@router.patch("/{pharmacy_id}",status_code=204)
async def update_pharmacy(pharmacy_id: str , payload: PharmacyUpdated):
   pharmacy_updated= await Pharmacy.get(pharmacy_id)
   if (payload.name):
       pharmacy_updated.name= payload.name
       
       
   if (payload.address):
       pharmacy_updated.address= payload.address
       
   if (payload.phone):
       pharmacy_updated.phone= payload.phone
       
   if (payload.localisation):
       pharmacy_updated.localisation= payload.localisation
    
   

      
   await pharmacy_updated.save()
   return 

#delete pharmacy 
@router.delete("/{pharmacy_id}", status_code=204)
async def delete_pharmacy(pharmacy_id: str):
   pharmacy_deleted= await Pharmacy.get(pharmacy_id)
   await pharmacy_deleted.delete()
   return 

#Function to verify that the product and pharmacy exist
async def check_pharmacy_and_product(pharmacy_id, product_id):
   
   #get pharmacy
   pharmacy= await Pharmacy.get(pharmacy_id)
   if not pharmacy:
      raise HTTPException(status_code=404, detail= "Pharmacy not found")
   
   #get product
   product= await Product.get(product_id)
   if not product:
      raise HTTPException(status_code=404, detail="Product not found")
   return
   
   
    
#Get all product in a pharmacy
@router.get("/{pharmacy_id}/products", status_code=200)
async def get_all_products_in_pharmacy(pharmacy_id: str) -> List [ProductInPharmacy] :
   pharmacy= await Pharmacy.get(pharmacy_id)
   if not pharmacy:
      raise HTTPException(status_code=404, detail= "Pharmacy not found")
   
   productsInPharmacy= await ProductInPharmacy.find(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), fetch_links=True,).to_list()
   return productsInPharmacy

#Post a product in a pharmacy
@router.post("/{pharmacy_id}/products/{product_id}", status_code=201, response_model=dict)
async def add_product_to_pharmacy(pharmacy_id: str, product_id: str, payload:ProductInPharmacyAdd):
   await check_pharmacy_and_product(pharmacy_id, product_id) #To verify that the product and pharmacy exist
   productInPharmacy = ProductInPharmacy(product= product_id, pharmacy= pharmacy_id, price= payload.price, quantity= payload.quantity)
   await productInPharmacy.create() 
   return {"message": "Added succesfullyw"}



#Get product by id a pharmacy
@router.get("/{pharmacy_id}/products/{product_id}", status_code=200)
async def get_product_by_id_in_pharmacy(pharmacy_id: str, product_id: str) -> Product :
   await check_pharmacy_and_product (pharmacy_id, product_id) #To verify that the product and pharmacy exist
   productInPharmacy = await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), ProductInPharmacy.product.id == ObjectId(product_id))
   productInPharmacy= ProductInPharmacy.get(product_id)
   return productInPharmacy

#update product in a pharmacy
@router.patch("/{pharmacy_id}/products/{product_id}", status_code=200)
async def update_product_in_pharmacie(pharmacy_id: str, product_id: str , payload: ProductInPharmacyUpdate):
   await check_pharmacy_and_product(pharmacy_id, product_id)
   productInPharmacy = await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), ProductInPharmacy.product.id == ObjectId(product_id))
   if (payload.price):
      productInPharmacy.price=payload.price

   if (payload.quantity):
      productInPharmacy.quantity=payload.quantity
     
   
      
   await productInPharmacy.save()
   return 

#delete product in a pharmacy
@router.delete("/{pharmacy_id}/products/{product_id}")
async def delete_product_in_pharmacy(pharmacy_id,product_id: str):
   await check_pharmacy_and_product(pharmacy_id, product_id)
   productInPharmacy = await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), ProductInPharmacy.product.id == ObjectId(product_id))
   await productInPharmacy.delete()
   return 
    
      
    
    
      
    
        