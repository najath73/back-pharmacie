import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId
from models.pharmacy import Pharmacy
from pymongo.errors import DuplicateKeyError
from models.user import CustomerUserCreate, User, UserCreate, UserUpdate, UserRole, Customer, PharmacyEmploye, SuperAdmin
from utils.auth import get_password_hash
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[User])
async def get_users():
   logger.info("Fetching all users")
   users = await User.find_all().to_list()
   return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: PydanticObjectId):
   logger.info(f"Fetching user with ID: {user_id}")
   user = await User.get(user_id)
   if user is None:
      logger.error(f"User not found with ID: {user_id}")
      raise HTTPException(status_code=404, detail="User not found")
   return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: PydanticObjectId, updated_user: UserUpdate):
   logger.info(f"Updating user with ID: {user_id}")
   user = await User.get(user_id)
   if user is None:
      logger.error(f"User not found with ID: {user_id}")
      raise HTTPException(status_code=404, detail="User not found")
   
   update_data = updated_user.dict(exclude_unset=True)
   for key, value in update_data.items():
      setattr(user, key, value)
   
   await user.save()
   logger.info(f"User updated with ID: {user.id}")
   return user

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: PydanticObjectId):
   logger.info(f"Deleting user with ID: {user_id}")
   user = await User.get(user_id)
   if user is None:
      logger.error(f"User not found with ID: {user_id}")
      raise HTTPException(status_code=404, detail="User not found")
   await user.delete()
   logger.info(f"User deleted with ID: {user.id}")
   return user


async def create_user(user: UserCreate):
   try:
      logger.info(f"Creating user with username: {user.username}")
      new_user = User(
         username=user.username,
         email=user.email,
         hashed_password=user.password,  # You should hash the password before storing it
         role=user.role,
         first_name=user.first_name,
         last_name=user.last_name
      )
      await new_user.create()
      # Create a user based on the role
      if user.role == (UserRole.PHARMACY_EMPLOYEE or UserRole.PHARMACY_ADMIN) and user.pharmacy_id:
         new_user = PharmacyEmploye(user=new_user.id, pharmacy=user.pharmacy_id)
      elif user.role == UserRole.SUPER_ADMIN:
         new_user = SuperAdmin(user=new_user.id)
      elif user.role == UserRole.CUSTOMER:
         new_user = Customer(user=new_user.id)
      await new_user.insert()
      logger.info(f"User created with ID: {new_user.id}")
      return new_user
   except DuplicateKeyError as e:
      logger.error(f"Duplicate key error: {e}")
      raise HTTPException(status_code=400, detail="Username already exists")
   except Exception as e:
      logger.error(f"Error creating user: {e}")
      raise HTTPException(status_code=500, detail="Internal Server Error")

# Create a new user
@router.post("", response_model=SuperAdmin)
async def create_user_admin(user: UserCreate):
   logger.info(f"Creating user with username: {user.username}")
   user.password = get_password_hash(user.password)
   return await create_user(user)
 
@router.post("/customer", response_model=Customer)
async def create_customer(user: CustomerUserCreate):
   logger.info(f"Creating customer with email: {user.email}")
   if user.role != UserRole.CUSTOMER:
      logger.error("Invalid role for customer creation")
      raise HTTPException(status_code=400, detail="Invalid role for customer creation")
   user.password = get_password_hash(user.password)
   return await create_user(user)
