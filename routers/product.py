import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from models.product import Product, UpdateProduct, AddProduct
from models.pharmacy import Pharmacy

# Initialiser le logger
logging.basicConfig(level=logging.INFO)
router = APIRouter(prefix="/products", tags=["Products"])

# Get all products
@router.get("", status_code=200)
async def get_all_products(search: Optional[str] = Query(None, description="Search query to filter products by name")) -> List[Product]:
    try:
        if search:
            logging.info(f"Searching for products matching: {search}")
            # Rechercher les produits correspondant au critère de recherche
            products = await Product.find({"name": {"$regex": search, "$options": "i"}}).to_list()
        else:
            logging.info("Fetching all products")
            # Retourner tous les produits si aucune recherche n'est spécifiée
            products = await Product.find_all().to_list()
        
        logging.info(f"Found {len(products)} products")
        return products
    except Exception as e:
        logging.error(f"Error while fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching products")

# Post a product
@router.post("", status_code=201, response_model=dict)
async def post_a_product(payload: AddProduct):
    try:
        logging.info(f"Adding new product: {payload.name}")
        product_to_add = Product(
            name=payload.name,
            description=payload.description,
            img=payload.img,  # Correction: utiliser payload.img au lieu de payload.description
            pharmacy=payload.pharmacy_id,
            quantity=payload.quantity,
            price=payload.price
        )
        product_added = await product_to_add.create()
        logging.info(f"Product added successfully with ID: {product_added.id}")
        return {"message": "Product added successfully", "id": str(product_added.id)}
    except Exception as e:
        logging.error(f"Error while adding product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while adding product")

# Get product by ID
@router.get("/{product_id}", status_code=200)
async def get_product_by_id(product_id: str) -> Product:
    try:
        logging.info(f"Fetching product by ID: {product_id}")
        product = await Product.get(product_id)
        if not product:
            logging.warning(f"Product with ID {product_id} not found")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        logging.error(f"Error while fetching product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Update product
@router.patch("/{product_id}", status_code=204)
async def update_product(product_id: str, payload: UpdateProduct):
    try:
        logging.info(f"Updating product with ID: {product_id}")
        product_to_update = await Product.get(product_id)
        if not product_to_update:
            logging.warning(f"Product with ID {product_id} not found for update")
            raise HTTPException(status_code=404, detail="Product not found")

        if payload.name:
            product_to_update.name = payload.name
        if payload.description:
            product_to_update.description = payload.description
        if payload.quantity:
            product_to_update.quantity = payload.quantity
        if payload.price:
            product_to_update.price = payload.price
        if payload.img:
            product_to_update.img = payload.img

        await product_to_update.save()
        logging.info(f"Product with ID {product_id} updated successfully")
    except Exception as e:
        logging.error(f"Error while updating product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error while updating product: {str(e)}")

# Delete product
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
    try:
        logging.info(f"Deleting product with ID: {product_id}")
        product_to_delete = await Product.get(product_id)
        if not product_to_delete:
            logging.warning(f"Product with ID {product_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Product not found")

        await product_to_delete.delete()
        logging.info(f"Product with ID {product_id} deleted successfully")
    except Exception as e:
        logging.error(f"Error while deleting product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error while deleting product: {str(e)}")
