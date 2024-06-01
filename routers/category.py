from fastapi import APIRouter, HTTPException,status
from schemas import CategoryModel
from database.database import db
from database.models import Category
from fastapi.encoders import jsonable_encoder

category_router = APIRouter(prefix="/categories")

@category_router.post("/")
async def create_category(category:CategoryModel):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="category created")

@category_router.get("/")
async def get_categories():
    categories = db.query(Category).all()
    context = [
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ]
    return jsonable_encoder(context)

@category_router.get("/{id}")
async def category_detail(id:int):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    return jsonable_encoder(category)


@category_router.put("/{id}")
async def category_detail(id:int, category:CategoryModel):
    category_check = db.query(Category).filter(Category.id == id).first()
    if not category_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    for key, value in category.dict().items():
        setattr(category_check, key, value)

    db.add(category_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK,detail="updated")


@category_router.delete("/{id}")
async def delete_category(id:int):
    category_check = db.query(Category).filter(Category.id == id).first()
    if not category_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    db.delete(category_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="deleted")