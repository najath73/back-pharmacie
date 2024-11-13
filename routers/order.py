from typing import Annotated, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.order import Order, OrderLine, PostOrder, OrderUpdate
from models.product import Product
from models.pharmacy import Pharmacy
from models.user import User
from utils.auth import decode_access_token
import logging


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
async def create_order(order: PostOrder, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = decode_access_token(token).get("user_id")
    logger = logging.getLogger(__name__)

    logger.info(f"User {user_id} is creating an order")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = await User.get(ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")
    new_order =  Order(
        billing_address=order.billing_address,
        shipping_address=order.shipping_address,
        user_id=user.id
    )
    new_order = await new_order.insert()
    order_lines = []
    for item in order.products:
        product = await Product.get(item.product_id, fetch_links=True)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if item.quantity > product.stock:
            await new_order.delete()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
        product.stock -= item.quantity
        await product.save()
        order_line = OrderLine(
            product_id=product.id,
            quantity=item.quantity,
            order=new_order.id,
            pharmacy_id=product.pharmacy.id
        )
        order_line= await order_line.insert()
        order_lines.append(order_line)
    new_order.order_lines = order_lines
    await new_order.save()
    return new_order

# Get all user orders
@router.get("/", response_model=List[Order])
async def get_user_orders(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = decode_access_token(token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    orders = await Order.find({"user_id": ObjectId(user_id)},fetch_links=True).to_list()
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, order_update: OrderUpdate, token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)

    await order.save()
    return order


@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await order.delete()
    return {"message": "Order deleted successfully"}