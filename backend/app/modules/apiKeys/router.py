from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.apiKeys.schemas import ApiKeyCreate, ApiKeyCreatedResponse, ApiKeyResponse
from app.modules.apiKeys.service import ApiKeyService

router = APIRouter(prefix="/api-keys", tags=["api-keys"])

@router.get("/", response_model=List[ApiKeyResponse])
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = ApiKeyService(db)
    return service.list_keys(current_user)

@router.get("/{key_id}", response_model=ApiKeyResponse)
def get(key_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = ApiKeyService(db)
    return service.get_key(key_id, current_user)


@router.post("/create", response_model=ApiKeyCreatedResponse, status_code=201)
def create(key_in: ApiKeyCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:create"))):
    """
    Cria uma nova chave.
    A chave completa é retornada UMA ÚNICA VEZ.
    """
    service = ApiKeyService(db)
    return service.create(key_in, current_user)


@router.patch("/{key_id}", response_model=ApiKeyResponse)
def toggle(key_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:update"))):
    """Liga ou desliga uma chave."""
    service = ApiKeyService(db)
    return service.toggle_active(key_id, current_user)


@router.delete("/{key_id}", status_code=204)
def delete(key_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:delete"))):
    service = ApiKeyService(db)
    service.delete(key_id, current_user)