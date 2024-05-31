from fastapi import APIRouter, HTTPException, status
from schemas import ProductModel
from database.database import db
from database.models import Product, Category
from fastapi.encoders import jsonable_encoder

product_router = APIRouter(prefix="/products")


@product_router.post("/")
async def create_product(product: ProductModel):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if category:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id,
        )
        db.add(new_product)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="product created")
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating a product"
    )


@product_router.get("/")
async def get_products():
    products = db.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
        }
        for product in products
    ]
    return jsonable_encoder(context)
