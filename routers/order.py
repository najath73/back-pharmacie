from typing import Annotated, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.order import Order, PostOrder, ProductInOrder, OrderUpdate
from models.product import Product
from models.pharmacy import Pharmacy
from models.user import User
from utils.auth import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/orders", tags=["Orders"])

#Get all oder 
@router.get("", status_code=200)
async def get_all_order_in_pharmacie() -> List [Order]:
    orders= await Order.find_all().to_list()
    return orders



#Get all user's order
@router.get("/users", status_code=200)
async def get_all_user_order( token: Annotated[str, Depends(oauth2_scheme)]):
    user_email = decode_access_token(token=token)
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    
    print(user)
    orders= await Order.find(Order.user.id== ObjectId(user.id)).to_list()
    print(orders)
    return orders
    





#Update order status
@router.patch("/{order_id}",status_code=204)
async def update_order(order_id: str , payload: OrderUpdate):
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=" Order not found")
    
    order.status = payload.status
    await order.save()
    return
        
       
     
# Récupérer les commandes d'une pharmacie
@router.get("/pharmacy/{pharmacy_id}", response_model=List[Order])
async def get_pharmacy_orders(pharmacy_id: str):
    pharmacy = await Pharmacy.get((pharmacy_id))
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    # Récupérer toutes les commandes
    pharmacy_orders = await Order.find(Order.pharmacy.id == ObjectId(pharmacy_id)).to_list()



    return pharmacy_orders



# Get order by ID
@router.get("/{order_id}",  status_code=200)
async def get_order_by_id(order_id: str) -> Order:
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
