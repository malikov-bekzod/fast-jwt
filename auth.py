from fastapi import APIRouter,HTTPException,status
from schemas import RegisterModel,LoginModel
from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash,check_password_hash

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register")
def register(user: RegisterModel):
    check_user_by_username = db.query(User).filter(User.username == user.username).first()
    check_user_by_email = db.query(User).filter(User.email == user.email).first()
    # print(check_user_by_username,check_user_by_email)
    if check_user_by_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username already in use")
    if check_user_by_email:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already in use")
        
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="successfully signed up")

@auth_router.post("/login")
def register(user: LoginModel):
    check_user = db.query(User).filter(User.username == user.username).first()
    if check_user:
        if check_password_hash(check_user.password ,user.password):
            return {"status_code": "200", "detail":"you're logged in"}
        return {"status_code": "400", "detail":"username or password wrong"}
    return {"status_code": "400", "detail":"username or password wrong"}