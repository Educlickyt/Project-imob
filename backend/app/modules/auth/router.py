from fastapi import APIRouter, Depends, Request
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

@router.post("/refresh")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    token_str = request.cookies.get("refresh_token")
    
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(token_str)

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    
    auth_service = AuthService(db)
    return auth_service.logout_user(refresh_token)

@router.post("/logout/all")
def logout_all(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    
    auth_service = AuthService(db)
    return auth_service.logout_all_user(refresh_token)