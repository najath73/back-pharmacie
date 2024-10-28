import logging
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from models.product import Category, Product, UpdateProduct, AddProduct
from models.pharmacy import Pharmacy
from models.user import PharmacyEmploye, User, UserRole
from utils.auth import get_current_user
from utils.services import fetch_products, fetch_product_by_id, fetch_pharmacy_by_id

# Initialize the logger
logging.basicConfig(level=logging.INFO)
router = APIRouter(prefix="/products", tags=["Products"])



# Endpoint to get all products, optionally filtered by a search query
@router.get("", status_code=200)
async def get_all_products(search: Optional[str] = Query(None, description="Search query to filter products by name")) -> List[Product]:
    try:
        products = await fetch_products(search)
        logging.info(f"Found {len(products)} products")
        return products
    except Exception as e:
        logging.error(f"Error while fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching products")

# Endpoint to add a new product
@router.post("", status_code=201, response_model=dict)
async def post_a_product(payload: AddProduct, current_user: User = Depends(get_current_user)):

    logging.info(f"Adding new product: {payload.name}")
    pharmacy = await fetch_pharmacy_by_id(payload.pharmacy_id)
    category = await Category.get(payload.category_id)
    if not category:
        logging.error(f"Category with ID {payload.category_id} not found")
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        new_product = Product(
            name=payload.name,
            description=payload.description,
            img=payload.img,
            stock=payload.stock,
            price=payload.price,
            pharmacy=pharmacy,
            prescription=payload.prescription,
            category=category
        )
        await new_product.save()
        logging.info(f"Product {payload.name} added successfully")
        return {"message": "Product added successfully", "id": str(new_product.id)}
    except Exception as e:
        logging.error(f"Error while adding product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while adding product")
    
# Endpoint to get a product by its ID
@router.get("/{product_id}", status_code=200, response_model=Product)
async def get_product_by_id(product_id: str):
    try:
        logging.info(f"Fetching product by ID: {product_id}")
        return await fetch_product_by_id(product_id)
    except Exception as e:
        logging.error(f"Error while fetching product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoint to update a product by its ID
@router.patch("/{product_id}", status_code=204)
async def update_product(product_id: str, payload: UpdateProduct, current_user: User = Depends(get_current_user)):
    try:
        logging.info(f"Updating product with ID: {product_id}")
        product = await fetch_product_by_id(product_id)
        update_data = {key: value for key, value in payload.dict().items() if value is not None}
        await product.update({"$set": update_data})
        logging.info(f"Product with ID {product_id} updated successfully")
    except Exception as e:
        logging.error(f"Error while updating product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error while updating product: {str(e)}")

# Endpoint to delete a product by its ID
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str, current_user: User = Depends(get_current_user)):
    product = await fetch_product_by_id(product_id)
    if current_user.role == UserRole.CUSTOMER or current_user.role == UserRole.PHARMACY_EMPLOYEE:
        logging.error(f"Unauthorized access attempt by user: {current_user.username}")
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    
    if current_user.role == UserRole.PHARMACY_ADMIN:
      employeInfo = await PharmacyEmploye.find_one(PharmacyEmploye.user.id == ObjectId(current_user.id), fetch_links=True)
      if employeInfo.pharmacy.id != ObjectId(product.pharmacy.id):
         print(employeInfo.pharmacy.id)
         logging.error(f"Unauthorized access attempt by user: {current_user.username}")
         raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    try:
        logging.info(f"Deleting product with ID: {product_id}")
        product = await fetch_product_by_id(product_id)
        await product.delete()
        logging.info(f"Product with ID {product_id} deleted successfully")
    except Exception as e:
        logging.error(f"Error while deleting product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error while deleting product: {str(e)}")
