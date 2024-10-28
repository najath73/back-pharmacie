from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from pymongo.errors import DuplicateKeyError
from models.pharmacy import Pharmacy, PharmacyUpdated
from models.product import Product
from models.user import PharmacyEmploye, PharmacyUserCreate, User, UserCreate, UserRole
from routers.user import create_user
from utils.auth import  generate_password, get_current_user, get_password_hash
from utils.email import send_registration_email
from utils.services import fetch_pharmacy_by_id
import logging
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the API router with a prefix and tags
router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("", status_code=200)
async def get_all_pharmacies() -> List[Pharmacy]:
   """
   Fetch all pharmacies from the database.
   """
   logger.info("Fetching all pharmacies")
   return await Pharmacy.find_all().to_list()

# Add a new pharmacy to the database
@router.post("", status_code=201, response_model=dict)
async def post_a_pharmacy(payload: Pharmacy, current_user: User = Depends(get_current_user)):
   """
   Add a new pharmacy to the database.
   """
   if current_user.role != UserRole.SUPER_ADMIN:
      logger.error("Unauthorized access attempt by user: {current_user.username}")
      raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
   try:
      logger.info(f"Adding a new pharmacy with name: {payload.name}")
      pharmacy_added = await payload.create()
   except DuplicateKeyError as e:
      error_message = e.details.get('errmsg', str(e))
      logger.error(f"Duplicate entry detected: {error_message}")
      raise HTTPException(status_code=400, detail={
         "error_description": "Duplicate entry detected",
         "error_message": error_message
      })
   return {"message": "Pharmacy added successfully", "id": str(pharmacy_added.id)}

# Fetch a pharmacy by its ID
@router.get("/{pharmacy_id}", status_code=200)
async def get_pharmacy_by_id(pharmacy_id: str) -> Pharmacy:
   """
   Fetch a pharmacy by its ID.
   """
   logger.info(f"Fetching pharmacy with id: {pharmacy_id}")
   pharmacy = await fetch_pharmacy_by_id(pharmacy_id)
   return pharmacy

# Update an existing pharmacy's details
@router.patch("/{pharmacy_id}", status_code=204)
async def update_pharmacy(pharmacy_id: str, payload: PharmacyUpdated, current_user: User = Depends(get_current_user)):
   """
   Update an existing pharmacy's details.
   """
   logger.info(f"role: {current_user.role}")
   if current_user.role == UserRole.CUSTOMER or current_user.role == UserRole.PHARMACY_EMPLOYEE:
      logger.error(f"Unauthorized access attempt by user: {current_user.username}")
      raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
   
   if current_user.role == UserRole.PHARMACY_ADMIN:
      employeInfo = await PharmacyEmploye.find_one(PharmacyEmploye.user.id == ObjectId(current_user.id), fetch_links=True)
      if employeInfo.pharmacy.id != ObjectId(pharmacy_id):
         print(employeInfo.pharmacy.id)
         logger.error(f"Unauthorized access attempt by user: {current_user.username}")
         raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
   logger.info(f"Updating pharmacy with id: {pharmacy_id}")
   pharmacy = await fetch_pharmacy_by_id(pharmacy_id)
   update_data = {key: value for key, value in payload.dict().items() if value is not None}
   await pharmacy.update({"$set": update_data})

# Delete a pharmacy by its ID
@router.delete("/{pharmacy_id}", status_code=204)
async def delete_pharmacy(pharmacy_id: str, current_user: User = Depends(get_current_user)):
   """
   Delete a pharmacy by its ID.
   """
   logger.info(f"role: {current_user.role}")
   if current_user.role != UserRole.SUPER_ADMIN:
      logger.error(f"Unauthorized access attempt by user: {current_user.username}")
      raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
   logger.info(f"Deleting pharmacy with id: {pharmacy_id}")
   pharmacy = await fetch_pharmacy_by_id(pharmacy_id)
   await pharmacy.delete()

# Add a new product to a specific pharmacy
@router.get("/{pharmacy_id}/products", status_code=200, response_model=List[Product])
async def get_all_products_in_pharmacy(pharmacy_id: str) -> List[Product]:
   """
   Fetch all products for a specific pharmacy.
   """
   logger.info(f"Fetching all products for pharmacy with id: {pharmacy_id}")
   pharmacy = await fetch_pharmacy_by_id(pharmacy_id)
   return await Product.find(Product.pharmacy.id == ObjectId(pharmacy_id), fetch_links=True).to_list()

# Fetch all users for a specific pharmacy
@router.get("/{pharmacy_id}/users", status_code=200, response_model=List[PharmacyEmploye])
async def get_user_for_a_pharmacy(pharmacy_id: str, current_user: User = Depends(get_current_user)):
   """
   Fetch all users for a specific pharmacy.
   """
   pharmacy = await fetch_pharmacy_by_id(pharmacy_id)
   print(pharmacy.id)
   return await PharmacyEmploye.find(PharmacyEmploye.pharmacy.id == pharmacy.id, fetch_links= True).to_list()


# Add a user to a specific pharmacy
@router.post("/{pharmacy_id}/users", status_code=201, response_model=dict)
async def add_user_to_pharmacy(pharmacy_id: str, payload: PharmacyUserCreate):
   """
   Add a new user to a specific pharmacy.
   """
   # Validate email address
   if "@" not in payload.email:
      raise HTTPException(status_code=400, detail="Invalid email address")

   # Call the create_user function to create a new user
   
   user_payload = UserCreate(
      username=payload.username,
      email=payload.email,
      password=get_password_hash(payload.password),
      role=payload.role,
      first_name=payload.first_name,
      last_name=payload.last_name,
      pharmacy_id=pharmacy_id
   )
   print(user_payload)
   new_user = await create_user(user_payload)
   # Send registration email to the new user
   send_registration_email(payload.email, payload.username, payload.password)
   return {"message": "User added successfully", "new_user": (new_user)}
   