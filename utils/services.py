from typing import Optional, List
import logging
from fastapi import HTTPException

from models.product import Product
from models.pharmacy import Pharmacy

# Fetch products from the database, optionally filtering by a search query
async def fetch_products(search: Optional[str] = None) -> List[Product]:
    if search:
        logging.info(f"Searching for products matching: {search}")
        return await Product.find({"name": {"$regex": search, "$options": "i"}}).to_list()
    logging.info("Fetching all products")
    return await Product.find_all().to_list()

# Fetch a single product by its ID
async def fetch_product_by_id(product_id: str) -> Product:
    product = await Product.get(product_id, fetch_links=True)
    if not product:
        logging.warning(f"Product with ID {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Fetch a pharmacy by its ID
async def fetch_pharmacy_by_id(pharmacy_id: str) -> Pharmacy:
    pharmacy = await Pharmacy.get(pharmacy_id)
    if not pharmacy:
        logging.warning(f"Pharmacy with ID {pharmacy_id} not found")
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy