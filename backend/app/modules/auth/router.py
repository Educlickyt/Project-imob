from fastapi import APIRouter, Depends
from app.modules.auth.schemas import RegisterRequest, LoginRequest, Token
from app.modules.auth.service import AuthService

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.authenticate_user(user_credentials.email, user_credentials.password)


@router.post("/register", response_model=dict, status_code=201)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_tenant(user_data)