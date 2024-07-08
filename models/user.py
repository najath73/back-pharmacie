
from enum import Enum
from typing import List, Optional
from beanie import Document, Indexed
from pydantic import BaseModel


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
    roles: List[Role]

    class Settings:
        name = "users"
        
class UserUpdate(BaseModel):
    username: Optional[str] 
    password:Optional [str]