from typing import List

from fastapi import APIRouter, HTTPException

from models.order import OrderInPharmacy, OrderUpdate
from models.user import User



router = APIRouter(prefix="/order", tags=["Order"])

#Get all oder in pharmacie
@router.get("", status_code=200)
async def get_all_order_in_pharmacie() -> List [OrderInPharmacy]:
    order= await OrderInPharmacy.find_all().to_list()
    return order

#Post  oder in pharmacie
@router.post("", status_code=201, response_model=dict)
async def post_order_in_pharmacy(payload: OrderInPharmacy):
    order = await payload.create()
    return {"message": "Order added successufuly", "id": str(order.id)}



#Update pharmacy
@router.patch("/{ordr_id}",status_code=204)
async def update_order(order_id: str , payload: OrderUpdate):
   order= await OrderInPharmacy.get(order_id)
   if (payload.productInOrder):
       order.productInOrder= payload.productInOrder
       
       

    
   

      
   await order.save()
   return 

  
  
#delete order 
@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
   order= await OrderInPharmacy.get(order_id)
   await order.delete()
   return  

#Get order by user_id
@router.get("/users/{user_id}", status_code=200)
async def get_order_by_user_id(user_id: str) -> OrderInPharmacy:
    user= await User.get(user_id)
    if not user:
      raise HTTPException(status_code=404, detail= "User not found")
    





