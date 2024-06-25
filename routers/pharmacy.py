from fastapi import APIRouter

from models.pharmacy import Pharmacy, UpdatePharmacy

router = APIRouter(prefix="/pharmacy", tags=["Pharmacies"])

#Get all pharmacy
@router.get("", status_code=200,response_model=list)
async def get_all_pharmacies():
    pharmacy= await Pharmacy.find_all().to_list()
    return pharmacy

#Post a pharmacy
@router.post("", status_code=201, response_model=dict)
async def post_a_pharmacy(payload: Pharmacy):
    prharmacy_created= await payload.create()
    return {"message": "Pharmacy added successfully", "id":prharmacy_created.id}

#Get pharmacy by id
@router.get("/{pharmacy_id}",status_code=200)
async def get_pharmacy_by_id(pharmacy_id: str) ->Pharmacy:
    pharmacy= await Pharmacy.get(pharmacy_id)
    return pharmacy

#Update pharmacy
@router.patch("/{pharmacy_id}")
async def update_pharmacy(pharmacy_id: str , payload: UpdatePharmacy):
   pharmacy= await Pharmacy.get(pharmacy_id)
   if (payload.name):
       pharmacy.name= payload.name
       
       
   if (payload.adress):
       pharmacy.adress= payload.adress
       
   if (payload.phone):
       pharmacy.phone= payload.phone
       
   if (payload.localisation):
       pharmacy.localisation= payload.localisation
    
   if (payload.products):
       pharmacy.products = payload.products
       

      
   await pharmacy.save()
   return 

#delete pharmacy 
@router.delete("/{pharmacy_id}")
async def delete_pharmacy(pharmacy_id: str):
   pharmacy= await Pharmacy.get(pharmacy_id)
   await pharmacy.delete()
   return {"message":"Pharmacy deleted successfully"}
    
    
      
    
    
      
    
        