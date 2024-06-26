
from typing import Optional
from beanie import Document


class User(Document):
    username: str
    name: str
    firstname: str
    email: str
    password: str
    role: str

    class Settings:
        name = "utilisateur"
        
class UserUpdate(Document):
    username: Optional[str] 
    password:Optional [str]