from fastapi import APIRouter




router = APIRouter(prefix="/produit")


produits= [
   {
       "id": 1,
       "name": "Donka"
   },
   {
       "id": 1,
       "name": "Donka"
   }
]


#Get all produits
@router.get("")
async def get_produits():
   return produits


#post a pharmacie
@router.post("")
async def post_produit(payload: dict):
   return produits


#get by id a pharmacie
@router.get("/{produit_id}")
async def post_pharmacie(produit_id: str):
   return produit_id
