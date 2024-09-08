
from enum import Enum
from typing import List, Optional
from beanie import Document, Indexed, Link
from pydantic import BaseModel

from models.pharmacy import Pharmacy


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    SIMPLE_USER= "simple_user"
    PHARMACY_MANAGER = "pharmacy_manager"
    PHARMACY_WORKER = "pharmacy_worker"


class User(Document):
    username: Indexed(str, unique=True) # type: ignore
    name: str
    firstname: str
    email: Indexed(str, unique=True) # type: ignore
    password: str
    roles: Role
    pharmacy: Optional[Link[Pharmacy]] = None

    class Settings:
        name = "users"
        
class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[Role] = None

class PostUserToPharmacy(BaseModel):
    username: Indexed(str, unique=True) # type: ignore
    name: str
    firstname: str
    email: Indexed(str, unique=True) # type: ignore
    password: Optional[str] = None
    roles: Role

class UserPharmacyInfo(BaseModel):
    id: str
    name: str
class UserInfo(BaseModel):
    id: str
    username: str
    name: str
    firstname: str
    email: str
    roles: str
    pharmacy: Optional[UserPharmacyInfo]  # Si tu souhaites inclure des informations sur la pharmacie
