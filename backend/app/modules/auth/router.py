from fastapi import APIRouter, Depends
from app.modules.auth.schemas import UserCreate, UserResponse
from app.modules.auth.service import AuthService

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login():
    return {"message": "login efetuado"}

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)
    