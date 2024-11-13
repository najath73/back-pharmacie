from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from enum import Enum
from models.pharmacy import Pharmacy
from models.product import Product
from models.user import Customer, User


class StatusOrder(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
# OrderLine Model: Each line represents a product in an order
class OrderLine(Document):
    product_id: Link[Product]
    quantity: int
    pharmacy_id: Link[Pharmacy]
    order: Link["Order"]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "order_lines"

# Order Model: Each order has multiple order lines
class Order(Document):
    order_lines: List[Link[OrderLine]] = None  # List of OrderLine IDs
    billing_address: str
    shipping_address: str
    user_id: Link[User]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "orders"
    
    class Config:
        schema_extra = {
            "example": {
                "id": "13HJJER8HH!888U",
                "order_lines": ["13HJJER8HH!888U", "13HJJER8HH!888U"],
                "billing_address": "2 carrefour du matin",
                "shipping_address": "2 carrefour du matin",
                "customer_id": "13HJJER8HH!888U",
                "pharmacy_id": "13HJJER8HH!888U",
                "created_at": "2022-01-01T00:00:00"
            }
        }

class PostOrderLine(BaseModel):
    product_id: str
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "product_id": "13HJJER8HH!888U",
                "quantity": 2
            }
        }

class PostOrder(BaseModel):
    products: List[PostOrderLine]
    billing_address: str
    shipping_address: str
    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "product_id": "13HJJER8HH!888U",
                        "quantity": 2
                    },
                    {
                        "product_id": "13HJJER8HH!888U",
                        "quantity": 3
                    }
                ],
                "billing_address": "2 carrefour du matin",
                "shipping_address": "2 carrefour du matin",
                "pharmacy_id": "13HJJER8HH!888U"
            }
        }

class OrderUpdate(BaseModel):
    status: Optional[StatusOrder] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    pharmacy_id: Optional[str] = None
    customer_id: Optional[str] = None
    order_lines: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        schema_extra = {
            "example": {
                "status": "pending",
                "billing_address": "2 carrefour du matin",
                "shipping_address": "2 carrefour du matin",
                "pharmacy_id": "13HJJER8HH!888U",
                "customer_id": "13HJJER8HH!888U",
                "order_lines": ["13HJJER8HH!888U", "13HJJER8HH!888U"],
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00"
            }
        }