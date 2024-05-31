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