
from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel


class User(Document):
    username: Indexed(str, unique=True)
    name: str
    firstname: str
    email: Indexed(str, unique=True)
    password: str
    role: str

    class Settings:
        name = "users"
        
class UserUpdate(BaseModel):
    username: Optional[str] 
    password:Optional [str]