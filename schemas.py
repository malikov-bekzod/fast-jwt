from pydantic import BaseModel, Field

class RegisterModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True



class CategoryModel(BaseModel):
    name: str

    class Config:
        orm_mode = True



class ProductModel(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

    class Config:
        orm_mode = True



class OrderModel(BaseModel):
    product_id: int
    user_id: int

    class Config:
        orm_mode = True