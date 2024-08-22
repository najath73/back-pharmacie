from typing import Annotated, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.order import Order, PostOrder, ProductInOrder, OrderUpdate
from models.product import Product
from models.pharmacy import ProductInPharmacy
from models.user import User
from utils.auth import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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
async def post_order_in_pharmacy(payload: PostOrder, token: Annotated[str, Depends(oauth2_scheme)]):
    

    user_email = decode_access_token(token=token)
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    listOfProductsInOrder = []
    for item in payload.producstInOrder:
        productInPharmacy = await ProductInPharmacy.find_one(ProductInPharmacy.pharmacy.id == ObjectId(item.pharmacy_id), ProductInPharmacy.product.id == ObjectId(item.product_id))
        if(productInPharmacy.quantity < item.quantity):
            raise HTTPException(status_code=400, detail="Quantité de produit indisponible en stock")
        producInOrder = ProductInOrder(productInPharmcy=productInPharmacy.id, quantity= item.quantity)
        producInOrderCreate= await producInOrder.create()
        listOfProductsInOrder.append(producInOrderCreate.id)
    print(listOfProductsInOrder)
    order = Order(productsInOrder=listOfProductsInOrder, user=user)
    orderCreate = await order.create()
    
    return {"message": "Order added successufuly", "id": str(orderCreate.id)}


#Add Product in  oder 



#Get all user's order
@router.get("/users/{user_id}", status_code=200)
async def get_all_user_order(user_id:str) -> List [Order]:
    user=await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders= await Order.find_all(Order.user.id== ObjectId(user.id)).to_list()
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
        
       
     





