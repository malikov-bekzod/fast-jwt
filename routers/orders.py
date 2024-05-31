from fastapi import APIRouter, HTTPException, status
from schemas import OrderModel
from database.database import db
from database.models import Product, User, Order
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix="/orders")


@order_router.post("/")
async def create_order(order: OrderModel):
    user = db.query(User).filter(User.id == order.user_id).first()
    product = db.query(Product).filter(Product.id == order.product_id).first()

    if user and product:
        new_order = Order(
            product_id=order.product_id,
            user_id=order.user_id,
        )
        db.add(new_order)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="order created")
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating a order"
    )


@order_router.get("/")
async def get_orders():
    orders = db.query(Order).all()
    context = [
        {
            "id": order.id,
            "product_id": order.product_id,
            "user_id": order.user_id
        }
        for order in orders
    ]
    return jsonable_encoder(context)
