from fastapi import APIRouter




router = APIRouter(prefix="/user")


users= [
   {
       "id": 1,
       "name": "Donka"
   },
   {
       "id": 1,
       "name": "Donka"
   }
]


#Get all users
@router.get("")
async def get_user():
   return users


#post a user
@router.post("")
async def post_user(payload: dict):
   return users


#get by id a user
@router.get("/{user_id}")
async def post_user(user_id: str):
   return user_id
