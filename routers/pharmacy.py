from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from models.pharmacy import Pharmacy, ProductInPharmacyAdd, PharmacyUpdated,ProductInPharmacyUpdate
from models.product import Product
from models.user import PostUserToPharmacy, User
from utils.auth import get_password_hash, generate_password
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

from utils.email import send_registration_email

load_dotenv()


router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

#Get all pharmacy
@router.get("", status_code=200)
async def get_all_pharmacies() -> List [Pharmacy]:
    pharmacy= await Pharmacy.find_all().to_list()
    return pharmacy

#Post a pharmacy
@router.post("", status_code=201, response_model=dict)
async def post_a_pharmacy(payload: Pharmacy):
   try:      
      pharmacy_added= await payload.create()
   except DuplicateKeyError as e:
        error_details = e.details
        error_message = error_details.get('errmsg', str(e))

        error_info = {
            "error_description": "Duplicate entry detected",
            "error_message": error_message          
        }
        raise HTTPException(status_code=400, detail=error_info)
      
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

   if (payload.img):
       pharmacy_updated.img= payload.img
       
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
async def get_all_products_in_pharmacy(pharmacy_id: str) -> List [Product] :
   pharmacy= await Pharmacy.get(pharmacy_id)
   if not pharmacy:
      raise HTTPException(status_code=404, detail= "Pharmacy not found")
   
   productsInPharmacy= pharmacy= await Product.find(Product.pharmacy.id == ObjectId(pharmacy_id),fetch_links=True).to_list()
   return productsInPharmacy
    
          
    
#post a user to a pharmacy
@router.post("/{pharmacy_id}/users",status_code=201, response_model=dict)
async def post_user_to_a_pharmacy(pharmacy_id: str, payload: PostUserToPharmacy):

   payload.password = generate_password()
   pswd_not_hash = (payload.password)
   payload.password= get_password_hash(payload.password)
   
   user_to_create = User(
      username=payload.username,
      name=payload.name,
      firstname=payload.firstname,
      email=payload.email,
      password=payload.password,
      roles=payload.roles,
      pharmacy=pharmacy_id  # Associe l'utilisateur à la pharmacie par l'ID
   )
   
   try:
      user_created= await user_to_create.create()

      # Envoi de l'email en utilisant la fonction séparée
      send_registration_email(payload.email, payload.username, pswd_not_hash)
   except DuplicateKeyError as e:
        error_details = e.details
        error_message = error_details.get('errmsg', str(e))

        error_info = {
            "error_description": "Duplicate entry detected",
            "error_message": error_message          
        }
        raise HTTPException(status_code=400, detail=error_info)

   return {"message": "User added successfully", "id": str(user_created.id)} 
    
#Get all user for a pharmacy
@router.get("/{pharmacy_id}/users",status_code=200, response_model=List[User])
async def get_user_for_a_pharmacy(pharmacy_id: str):

   #get pharmacy 
   pharmacy= await Pharmacy.get(pharmacy_id)
   if not pharmacy:
      raise HTTPException(status_code=404, detail= "Pharmacy not found")
   
   print(pharmacy_id)
   users= await User.find(User.pharmacy.id == ObjectId(pharmacy_id)).to_list()
   return users