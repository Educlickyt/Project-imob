from typing import List
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from app.modules.propertyOwners.repository import PropertyOwnerRepository
from app.modules.propertyOwners.schemas import PropertyOwnerCreate, PropertyOwnerUpdate, PropertyOwnerResponse
from app.modules.auth.schemas import TokenPayload
from app.modules.propertyOwners.models import PropertyOwner


class PropertyOwnerService:
    
    def __init__(self, db):
        self.propertyOwner_repo = PropertyOwnerRepository(db)
        
    def list_propertyOwners(self, current_user: TokenPayload) -> List[PropertyOwnerResponse]:
        propertyOwners = self.propertyOwner_repo.get_propertyOwners(current_user.tenant_id)
        
        if not propertyOwners:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Owners found."
            ) 
        return propertyOwners
    
    def get_by_id(self, propertyOwner_id: UUID, tenant_id) -> PropertyOwnerResponse:
        propertyOwner = self.propertyOwner_repo.get_by_id(propertyOwner_id, tenant_id)
        
        if not propertyOwner: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Owner not found."
            )
        return propertyOwner
    
    def create(self, propertyOwner_in: PropertyOwnerCreate, current_user: TokenPayload) -> PropertyOwnerResponse:
        
        propertyOwner_exists = self.propertyOwner_repo.get_by_email(propertyOwner_in.email, current_user.tenant_id)
        
        if propertyOwner_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This owner is already registered in the system."
            )
        
        propertOwner_data = propertyOwner_in.model_dump()
        propertOwner_data['tenant_id'] = current_user.tenant_id
        
        return self.propertyOwner_repo.create(propertOwner_data)
    
    def update(self, propertyOwner_id: UUID, propertyOwner_in:PropertyOwnerUpdate, current_user:TokenPayload) -> PropertyOwnerResponse:
        db_propertyOwner = self.get_by_id(propertyOwner_id, current_user.tenant_id)
        
        update_data = propertyOwner_in.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_propertyOwner
        
        return self.propertyOwner_repo.update(db_propertyOwner, update_data)
    
    def delete(self, propertyOwner_id: UUID, current_user: TokenPayload):
        db_propertyOwner = self.get_by_id(propertyOwner_id, current_user.tenant_id)
        
        self.propertyOwner_repo.update(db_propertyOwner, {"deleted_at": datetime.utcnow()})