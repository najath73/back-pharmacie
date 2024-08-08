from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import init_db
import routers.auth
import routers.order
import routers.pharmacy 
import routers.product
import routers.user



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield 
    print("Shutting down...")
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Ajouter les routers dédiés
app.include_router(routers.pharmacy.router)
app.include_router(routers.product.router)
app.include_router(routers.user.router)
app.include_router(routers.order.router)
app.include_router(routers.auth.router)