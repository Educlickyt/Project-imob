from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate
from app.modules.users.service import UserService
from app.modules.auth.dependencies import  PermissionChecker
from app.modules.auth.schemas import TokenPayload

from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("users:create"))):
    user_service = UserService(db)
    return user_service.create_user(user_data, current_user.tenant_id)

@router.get("/", response_model=List[UserResponse], status_code=200)
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("users:view"))):
    user_service = UserService(db)
    return user_service.list_users(current_user)

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get(user_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("users:view"))):
    user_service = UserService(db)
    return user_service.get_user(user_id, current_user)

@router.patch("/{user_id}", response_model=UserResponse, status_code=200)
def update(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("users:update"))):
    user_service = UserService(db)
    return user_service.update(user_id, user_data, current_user)

@router.delete("/{user_id}", status_code=204)
def delete(user_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("users:delete"))):
    user_service = UserService(db)
    return user_service.delete_user(user_id, current_user)
