from typing import List, Set
from beanie import Link, WriteRules
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from models.pharmacy import Pharmacy, PharmacyUpdated, ProductInPharmacyAdd, ProductInPharmacyUpdate, ProductInPharmacy
from models.product import Product



router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])



#Get all pharmacies
@router.get("", status_code=200)
async def get_pharmacies() -> List[Pharmacy]:
   pharmacies = await Pharmacy.find_all().to_list()
   return pharmacies


#post a pharmacy
@router.post("", status_code=201)
async def post_pharmacy(pharmacy: Pharmacy) :
   new_pharmacy = await pharmacy.create()
   return  {"message": "categorie ajouté avec succès"}


#get by id a pharmacy
@router.get("/{pharmacy_id}", status_code=200)
async def get_pharmacy_by_id(pharmacy_id: str)-> Pharmacy:
   pharmacy = await Pharmacy.get(pharmacy_id)
   return pharmacy


#update pharmacy by id
@router.patch("/{pharmacy_id}", status_code=204)
async def update_pharmacy(pharmacy_id: str, payload: PharmacyUpdated):
   pharmacy = await Pharmacy.get(pharmacy_id)
   if pharmacy is None:
      raise HTTPException (
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f'No corresponding pharmacy with id: {pharmacy_id}'
      )
   
   if(payload.name):
      pharmacy.name = payload.name
      await pharmacy.save()
   if(payload.address):
      pharmacy.address = payload.name
      await pharmacy.save()
   if(payload.phone):
      pharmacy.phone = payload.phone
      await pharmacy.save()
   if(payload.localisation):
      pharmacy.localisation = payload.localisation
      await pharmacy.save()
   return {"message": "Pharmacy updated successfuly"}

#delete pharmacy by id
@router.delete("/{pharmacy_id}", status_code=204)
async def delete_pharmacy(pharmacy_id: str):
   pharmacy = await Pharmacy.get(pharmacy_id)
   return {"message": "Pharmacy deleted successfully"}

async def check_product_and_pharmacy(pharmacy_id, product_id):
    pharmacy = await Pharmacy.get(pharmacy_id)
    if not pharmacy:
       raise HTTPException(status_code=404, detail="Pharmacy not found")

    product = await Product.get(product_id)
    if not product:
       raise HTTPException(status_code=404, detail="Product not found")
    return (pharmacy, product)
    
@router.post("/{pharmacy_id}/products/{product_id}")
async def add_product_for_a_pharmacy(pharmacy_id: str,product_id: str, payload: ProductInPharmacyAdd):

   phamacyProduct =await check_product_and_pharmacy(pharmacy_id, product_id)

   # Ajouter le produit à la liste des produits de la pharmacie
   productInpharmacy=  ProductInPharmacy(product=product_id, pharmacy=pharmacy_id, price=payload.price, quantity=payload.quantity)
   await productInpharmacy.create()
   return 



@router.patch("/{pharmacy_id}/products/{product_id}", status_code=204)
async def update_product_for_pharmacy(pharmacy_id: str, product_id: str, payload: ProductInPharmacyUpdate):

   await check_product_and_pharmacy(pharmacy_id, product_id)
   
   productInPharmacy =  await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), ProductInPharmacy.product.id == ObjectId(product_id))
   if(payload.quantity):
      productInPharmacy.quantity = payload.quantity
   if(payload.price):
      productInPharmacy.price = payload.price
   
   await productInPharmacy.save()
   return 

@router.delete("/{pharmacy_id}/products/{product_id}", status_code=204)
async def delete_product_for_pharmacy(pharmacy_id: str, product_id: str):

   await check_product_and_pharmacy(pharmacy_id, product_id)
   
   productInPharmacy = await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(pharmacy_id), ProductInPharmacy.product.id == ObjectId(product_id))
   
   await productInPharmacy.delete()
   return 

