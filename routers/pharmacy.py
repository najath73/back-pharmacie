from typing import List
from fastapi import APIRouter, HTTPException, status
from models.pharmacy import Pharmacy, PharmacyUpdated
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