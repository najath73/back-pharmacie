from datetime import datetime
from beanie import Document

class User(Document):
    username: str
    email: str
    password: str
    firstname: str
    lastname: str
    created_at: datetime = datetime.now()
