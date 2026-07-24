from typing import List 
from uuid import UUID

from fastapi import APIRouter,  Depends, HTTPException
from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.propertyOwners.schemas import PropertyOwnerResponse, PropertyOwnerCreate, PropertyOwnerUpdate
from sqlalchemy.orm import Session
from app.modules.propertyOwners.service import PropertyOwnerService


router = APIRouter(prefix="/propertyOwners", tags=['propertyOwners'])

@router.get('/', response_model=List[PropertyOwnerResponse])
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("propertyOwners:view"))):
    service = PropertyOwnerService(db)
    return service.list_propertyOwners(current_user)

@router.get('/{propertyOwner_id}')
def get(propertyOwner_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("propertyOwners:view"))):
    service = PropertyOwnerService(db)
    return service.get_by_id(propertyOwner_id, current_user.tenant_id)

@router.post('/create', response_model=PropertyOwnerResponse)
def create(propertyOwner_data: PropertyOwnerCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("propertyOwners:create"))):
    service = PropertyOwnerService(db)
    return service.create(propertyOwner_data, current_user)

@router.delete('/{propertyOwner_id}', status_code=204)
def delete(propertyOwner_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("propertyOwners:delete"))):
    service = PropertyOwnerService(db)
    service.delete(propertyOwner_id, current_user)

@router.patch('/{propertyOwner_id}', response_model=PropertyOwnerResponse)
def update(propertyOwner_id: UUID, propertyOwner_data: PropertyOwnerUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("propertyOwners:update"))):
    service = PropertyOwnerService(db)
    return service.update(propertyOwner_id, propertyOwner_data, current_user)
