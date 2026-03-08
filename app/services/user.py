# same as we have controllers file in js eco system
from fastapi import HTTPException
from app.schema.user import UserCreate 
from app.models.userModel import User
from app.db.session import SessionLocal
from app.services.emailService import (
    send_welcome_email,
    send_update_email,
    send_goodbye_email,
)

# to handle service for query update 
def create_user(name, email):
    db = SessionLocal()
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user


def create_user(data: UserCreate):     # ← receives the schema object
    db = SessionLocal()
    
    new_user = User(
        name=data.name,        # ← access like req.body.name
        email=data.email,      # ← access like req.body.email
        age=data.age           # ← access like req.body.age
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    send_welcome_email(name=new_user.name, email=new_user.email)
    return new_user

# def get_user():
#     return {"name": "Manthan", "role": "developer"}
def get_all():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def get_user(user_id: int):
    db = SessionLocal()
    
    # query() → SELECT * FROM users WHERE id = user_id
    user = db.query(User).filter(User.id == user_id).first()
    
    db.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


def update_user(user_id: int, name: str, email: str):
    db = SessionLocal()
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    old_name  = user.name
    old_email = user.email
    user.name = name        # update fields on the object
    user.email = email      # SQLAlchemy tracks these changes
    
    db.commit()             # UPDATE SQL runs here
    db.refresh(user)        # reload updated state from DB
    db.close()

    send_update_email(
        name=name,
        email=email,
        old_name=old_name,
        old_email=old_email,
    )

    return user


def delete_user(user_id: int):
    db = SessionLocal()
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    name  = user.name
    email = user.email

    db.delete(user)   # marks object for deletion
    db.commit()       # DELETE SQL runs here
    db.close()

    send_goodbye_email(name=name, email=email)
    
    return {"message": f"User {user_id} deleted successfully"}