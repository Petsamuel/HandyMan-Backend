# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database import get_db
from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, phone=user.phone, hashed_password = pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
