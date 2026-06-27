from uuid import UUID
from typing import List
from app.modules.propertyOwners.models import PropertyOwner

class PropertyOwnerRepository:
    
    def __init__(self,db):
        self.db = db
        
    def create(self, propertyOwner_data: dict) -> PropertyOwner:
        db_propertyOwner = PropertyOwner(**propertyOwner_data)
        self.db.add(db_propertyOwner)
        self.db.commit()
        self.db.refresh(db_propertyOwner)
        return db_propertyOwner
    
    def get_by_email(self, email: str, tenant_id: UUID) -> PropertyOwner | None:
        return self.db.query(PropertyOwner).filter(PropertyOwner.email == email, PropertyOwner.tenant_id == tenant_id, PropertyOwner.deleted_at.is_(None)).first()

    def get_by_id(self, propertyOwner_id: UUID, tenant_id: UUID) -> PropertyOwner | None:
        return self.db.query(PropertyOwner).filter(PropertyOwner.id == propertyOwner_id, PropertyOwner.tenant_id == tenant_id, PropertyOwner.deleted_at.is_(None)).first()
        
    
    def get_propertyOwners(self, tenant_id) -> List[PropertyOwner]:
        return self.db.query(PropertyOwner).filter(PropertyOwner.tenant_id == tenant_id, PropertyOwner.deleted_at.is_(None)).all()    
    
    def update(self, db_propertyOwner: PropertyOwner, update_data:dict):
        for key, value in update_data.items():
            setattr(db_propertyOwner, key, value)
        self.db.commit()
        self.db.refresh(db_propertyOwner)
        return db_propertyOwner
        