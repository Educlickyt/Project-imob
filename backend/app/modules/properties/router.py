from fastapi import APIRouter, Depends
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.properties.schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from app.modules.properties.service import PropertyService
from typing import List
from sqlalchemy.orm import Session
from app.core.dependencies import get_db

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model= PropertyResponse | List[PropertyResponse] ) #ADICIONAR PAGINAÇÃO
def get(property_id: str | None = None, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("role_create"))):
    
    property_service = PropertyService(db)
    return property_service.get_property(property_id)

@router.post("/create")
def create(property_data: PropertyCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:create"))):
    
    property_service = PropertyService(db)
    return property_service.create_property(property_data)

@router.post("/update")
def update(property_data: PropertyUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:update"))):
    property_service = PropertyService(db)
    return property_service.update_property(property_data)
    
    