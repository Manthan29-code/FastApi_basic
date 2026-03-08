# this is same page as we have routs page for each controls in js 

from fastapi import APIRouter
from fastapi import HTTPException
from app.services.user import create_user, get_user, update_user, delete_user , get_all
from app.schema.user import UserCreate , UserResponse

from typing import List
userRouter = APIRouter()

# post with query 
# @userRouter.post("/users")
# def add_user(name: str, email: str):          # ← these are QUERY params
#     return create_user(name, email)

# post with body  
@userRouter.post("/users"  , response_model=UserResponse)
def add_user(data: UserCreate):     # ← entire body maps to this object
    print(data.name)                # ← like req.body.name in JS
    print(data.email)               # ← like req.body.email in JS
    print(data.age)                 # ← like req.body.age in JS
    return create_user(data)


@userRouter.get("/users/{user_id}"  , response_model=UserResponse)
def fetch_user(user_id: int):                 # ← {user_id} is PATH param
    return get_user(user_id)


@userRouter.get("/allUsers", response_model=List[UserResponse])
def fetch_user():                 
    return get_all()


@userRouter.put("/users/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, name: str, email: str):
    return update_user(user_id, name, email)


@userRouter.delete("/users/{user_id}")
def remove_user(user_id: int):
    return delete_user(user_id)

@userRouter.get("/")
def home():
    return {"message": "API working 🚀"}

# @userRouter.get("/user")
# def user():
#     return get_user()