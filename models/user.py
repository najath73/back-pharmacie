from enum import Enum
from typing import List, Optional
from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr

from models.pharmacy import Pharmacy


class UserRole(str, Enum):
    CUSTOMER = "customer"
    PHARMACY_ADMIN = "pharmacy_admin"
    PHARMACY_EMPLOYEE = "pharmacy_employee"
    SUPER_ADMIN = "super_admin"  # Added SuperAdmin role

class User(Document):
    username: Indexed(str, unique=True) # type: ignore
    email: EmailStr
    hashed_password: str
    role: UserRole
    first_name: str  # Added first name
    last_name: str   # Added last name

    class Settings:
        collection = "users"

class Customer(Document):
    user: Link[User]

class PharmacyEmploye(Document):
    pharmacy: Link[Pharmacy]
    user : Link[User]

class SuperAdmin(Document):  # Added SuperAdmin class
    user: Link[User]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole
    first_name: str  # Added first name
    last_name: str   # Added last name
    pharmacy_id: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    first_name: Optional[str] = None  # Added first name
    last_name: Optional[str] = None   # Added last name
    pharmacy_id: Optional[str] = None



class UserInfo(BaseModel):
    username: str
    email: str
    role: UserRole
    first_name: str
    last_name: str



class PharmacyUserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.PHARMACY_EMPLOYEE
    first_name: str
    last_name: str


class CustomerUserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.CUSTOMER
    first_name: str
    last_name: str