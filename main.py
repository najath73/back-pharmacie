from fastapi import FastAPI
import routers.pharmacie 
import routers.router_produit 

app = FastAPI()




# Ajouter les routers dédiés
app.include_router(routers.router_pharmacie.router)
app.include_router(routers.router_produit.router)