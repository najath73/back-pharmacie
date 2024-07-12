
from enum import Enum
from typing import List, Optional
from beanie import Document, Indexed, Link
from pydantic import BaseModel

from models.pharmacy import Pharmacy


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    PHARMACY_MANAGER = "pharmacy_manager"
    PHARMACY_WORKER = "pharmacy_worker"


class User(Document):
    username: Indexed(str, unique=True)
    name: str
    firstname: str
    email: Indexed(str, unique=True)
    password: str
    roles: List[Role] = []
    pharmacy: Optional[Link[Pharmacy]] = None

    class Settings:
        name = "users"
        
class UserUpdate(BaseModel):
    username: Optional[str] 
    password:Optional [str]