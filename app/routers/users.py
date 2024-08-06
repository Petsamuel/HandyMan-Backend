from fastapi import APIRouter, Depends
from models.user import UserCreate, User
# from app.database import get_database

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    # Implement user creation logic
    return {"successful": user}
    pass