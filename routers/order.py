from typing import List

from fastapi import APIRouter, HTTPException

from models.order import Order, OrderInPharmacy, OrderUpdate, ProductInOrder, ProductInOrderUpdate
from models.user import User



router = APIRouter(prefix="/orders", tags=["Orders"])

#Get all oder 
@router.get("", status_code=200)
async def get_all_order_in_pharmacie() -> List [Order]:
    orders= await Order.find_all().to_list()
    return orders

# Get order by ID
@router.get("/{order_id}",  status_code=200)
async def get_order_by_id(order_id: str) -> Order:
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#Post  oder 
@router.post("", status_code=201, response_model=dict)
async def post_order_in_pharmacy(payload: Order):
    order = await payload.create()
    return {"message": "Order added successufuly", "id": str(order.id)}


#Add Product in  oder 



#Get all user's order
@router.get("/users/{user_id}", status_code=200)
async def get_all_user_order(user_id:str) -> List [Order]:
    user=await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders= await Order.find_all(Order.user==user_id).to_list()
    return orders
    





#Update  Product in order
@router.patch("/{ordr_id}",status_code=204)
async def update_order(order_id: str , payload: ProductInOrderUpdate):
   order= await Order.get(order_id)
   if not order:
        raise HTTPException(status_code=404, detail="Order not found")
   
   if (payload.quantity):
       order.quantity= payload.quantity
       await order.save()
       return
        
       
     

  
  
#delete order 
@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
   order= await Order.get(order_id)
   if not order:
        raise HTTPException(status_code=404, detail="Order not found")
   
   await order.delete()
   return  

#Delete Product in order
@router.delete("/{order_id}/productInOrder/{productInOrder_id}", status_code=204)
async def delete_item_from_order(order_id: str, productInOrder_id: str):
    productInOrder = await ProductInOrder.get(productInOrder_id)
    if not productInOrder or productInOrder.order.id != order_id:
        raise HTTPException(status_code=404, detail=" ProductInOrder not found")
    
    await productInOrder.delete()
    return
    





