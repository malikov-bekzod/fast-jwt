from fastapi import FastAPI
from database.database import engine
from database.database import Base
from routers.category import category_router
from routers.products import product_router
from routers.orders import order_router
from auth import auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(order_router)



