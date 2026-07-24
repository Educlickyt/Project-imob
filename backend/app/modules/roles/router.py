from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.auth.dependencies import PermissionChecker
from app.modules.auth.schemas import TokenPayload
from app.modules.roles.schemas import RoleCreate, RoleResponse, RoleCreateResponse, PermissionsResponse, RoleUpdate
from app.modules.roles.service import RoleService

from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get('/',response_model=List[RoleResponse], status_code=200)
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = RoleService(db)
    return service.list_roles(current_user)

@router.get('/permissions', response_model=List[PermissionsResponse], status_code=200)
def get(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = RoleService(db)
    return service.get_permissions(current_user)

@router.get('/{role_id}', response_model=RoleResponse, status_code=200)
def get(role_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = RoleService(db)
    return service.get_role(role_id, current_user)


@router.post('/create',response_model=RoleCreateResponse, status_code=201)
def create(role_data:RoleCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:create"))):   
    service = RoleService(db)
    return service.create_role(role_data, current_user.tenant_id)


@router.patch('/{role_id}',response_model=RoleCreateResponse, status_code=200)
def update(role_id: UUID, role_data: RoleUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:update"))):
    service = RoleService(db)
    return service.update_role(role_id, role_data, current_user)    
    

@router.delete('/{role_id}', status_code=204)
def delete(role_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:delete"))):
    service = RoleService(db)
    return service.delete_role(role_id, current_user)
    