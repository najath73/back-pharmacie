
from typing import Optional
from beanie import Document, Indexed


class User(Document):
    username: Indexed(str, unique=True)
    name: str
    firstname: str
    email: Indexed(str, unique=True)
    password: str
    role: str

    class Settings:
        name = "users"
        
class UserUpdate(Document):
    username: Optional[str] 
    password:Optional [str]