from typing import List
from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from models.user import User, UserUpdate
from utils.auth import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])



#Get all users
@router.get("",status_code=200)
async def get_all_user():
   users= await User.find_all().to_list()
   return users


#post a user
@router.post("",status_code=201, response_model=dict)
async def post_user(payload: User, ):
   payload.password= get_password_hash(User.password)

   try:
      user_created= await payload.create()
   except DuplicateKeyError as e:
        error_details = e.details
        error_message = error_details.get('errmsg', str(e))

        error_info = {
            "error_description": "Duplicate entry detected",
            "error_message": error_message          
        }
        raise HTTPException(status_code=400, detail=error_info)

   return {"message": "User added successfully", "id": str(user_created.id)} 


#get by id a user
@router.get("/{user_id}",status_code=200)
async def get_user_by_id(user_id: str):
   user= await User.get(user_id)
   return user

#update user
@router.patch("/{user_id}", status_code=204)
async def update_user(user_id: str,payload: UserUpdate):
   user_updated= await User.get(user_id)
   
   if(payload.username):
      user_updated.username= payload.username
   if(payload.password):
      user_updated.password= payload.password
      
   await user_updated.save()
   return{"message": "user updated successefuly"}

#user delete
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
   user_deleted= await User.get(user_id)
   await user_deleted.delete()
   return{"message": "User deleted succefully"}
   
