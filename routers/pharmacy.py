from fastapi import APIRouter




router = APIRouter(prefix="/pharmacies")


pharmacies= [
   {
       "id": 1,
       "name": "Donka"
   },
   {
       "id": 1,
       "name": "Donka"
   }
]


#Get all pharmacies
@router.get("")
async def get_pharmacie():
   return pharmacies


#post a pharmacie
@router.post("")
async def post_pharmacie(payload: dict):
   return pharmacies


#get by id a pharmacie
@router.get("/{pharmacie_id}")
async def post_pharmacie(pharmacie_id: str):
    return pharmacie_id
