from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import certifi

from models.order import Order, OrderLine
from models.pharmacy import Pharmacy
from models.product import Product, Category
from models.user import User, PharmacyEmploye, SuperAdmin, Customer
import os

from dotenv import load_dotenv

load_dotenv()


async def init_db():
    # Load the MongoDB connection string from the environment variable MONGODB_URI

    CONNECTION_STRING = os.getenv('DB_URL')

    # Create a MongoDB client
    client = AsyncIOMotorClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    await init_beanie(database=client.pharmaDB, document_models=[Product, Pharmacy, User, PharmacyEmploye, SuperAdmin, Order, OrderLine, Category, Customer])