from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import PermissionChecker, get_current_token_data
from app.modules.auth.schemas import TokenPayload
from app.modules.roles.schemas import RoleCreate, RoleResponse  
from app.modules.roles.service import RoleService

from uuid import UUID

from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post('/create',response_model=RoleResponse, status_code=201)
def create_role(role_data:RoleCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("role_create"))):   
    role_service = RoleService(db)
    return role_service.create_role(role_data, current_user.tenant_id)


@router.post('/update',response_model=dict, status_code=200)
def update_role(role_data:dict, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_token_data)):
    
    return {"user": current_user.sub}

@router.post('/delete',response_model=dict, status_code=200)
def delete_role(role_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_token_data)):
    
    return {"user": current_user.sub}

@router.get('/',response_model=dict, status_code=200)
def get_roles(name_role: str = None, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_token_data)):
    
    if name_role:
        return {"message": name_role}
    
    return {"user": current_user.sub}