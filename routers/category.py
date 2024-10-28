from typing import List
from fastapi import APIRouter, HTTPException
from models.product import Category
from pydantic import BaseModel

router = APIRouter(prefix="/categories", tags=["Categories"])
class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryUpdate(BaseModel):
    name: str = None
    description: str = None

# Get all categories
@router.get("", status_code=200)
async def get_all_categories() -> List[Category]:
    categories = await Category.find_all().to_list()
    return categories

# Get a single category by ID
@router.get("/{category_id}", status_code=200)
async def get_category(category_id: str) -> Category:
    category = await Category.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Create a new category
@router.post("", status_code=201)
async def create_category(category: CategoryCreate) -> Category:
    new_category = Category(**category.dict())
    await new_category.insert()
    return new_category

# Update an existing category
@router.put("/{category_id}", status_code=200)
async def update_category(category_id: str, category: CategoryUpdate) -> Category:
    existing_category = await Category.get(category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    updated_data = category.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(existing_category, key, value)
    await existing_category.save()
    return existing_category

# Delete a category
@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str):
    category = await Category.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await category.delete()
    return {"message": "Category deleted successfully"}