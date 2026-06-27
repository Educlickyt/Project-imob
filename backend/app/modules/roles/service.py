from fastapi import HTTPException, status
from app.modules.roles.repository import RoleRepository
from app.modules.roles.schemas import RoleCreate
from uuid import UUID


class RoleService:
    
    def __init__(self, db):
        self.role_repo = RoleRepository(db)
        
    def create_role(self, role_in: RoleCreate, tenant_id: UUID):
                
        role_exists = self.role_repo.get_by_name(role_in.name, tenant_id)
        
        if role_exists:
            raise HTTPException(    
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Essa role já existe"
            )
             
        role_data = role_in.model_dump()
        role_data['tenant_id'] = tenant_id
        
        return self.role_repo.create(role_data)