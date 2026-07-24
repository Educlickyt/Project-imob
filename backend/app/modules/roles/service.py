from fastapi import HTTPException, status
from app.modules.roles.repository import RoleRepository
from app.modules.roles.schemas import RoleCreate, RoleResponse, RoleCreateResponse
from uuid import UUID
from datetime import datetime, timezone

class RoleService:
    
    def __init__(self, db):
        self.role_repo = RoleRepository(db)
        
    def create_role(self, role_in: RoleCreate, tenant_id: UUID) -> RoleCreateResponse:
                
        role_exists = self.role_repo.get_by_name(role_in.name, tenant_id)
        
        if role_exists:
            raise HTTPException(    
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This role already exists"
            )
        
        permissions_data = self.role_repo.get_permissions()
        permissions = []
        for item in permissions_data:
            permissions.append(item.id)
        
        for permission in role_in.permissions:
            if permission not in permissions: 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Permissions not valid"
                )
        
        role_data = role_in.model_dump()
        role_data['tenant_id'] = tenant_id
        
        return self.role_repo.create(role_data)
    
    def list_roles(self, current_user):
        rows = self.role_repo.get_roles(current_user.tenant_id)
        
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Roles not found"
            )
            
         # Dicionário comum para agrupar
        roles_map = {}

        for role_id, name, description, perm_key in rows:
            # Converter UUID para string pra usar como chave
            rid = str(role_id)

            # Se essa role ainda não foi registrada, criar entrada
            if rid not in roles_map:
                roles_map[rid] = {
                    "id": role_id,
                    "name": name,
                    "description": description,
                    "permissions": []
                }

            if perm_key is not None:
                # Adicionar o nome da permissão na lista
                roles_map[rid]["permissions"].append(perm_key)

        # Montar a lista de respostas
        result = []
        for data in roles_map.values():
            result.append(RoleResponse(**data))

        return result

    def get_role(self, role_id: UUID, current_user):
        
        role_rows = self.role_repo.get_by_id_with_permissions(role_id, current_user.tenant_id)
        
        if not role_rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )
        
        role = {
            "id": None,
            "name": None,
            "description": None,
            "permissions": []
        }
        
        for id, name, description, key in role_rows:
            role["id"] = id
            role["name"] = name
            role["description"] = description
            if key is not None:
                role["permissions"].append(key)       
            
        return role
    
    def get_permissions(self, current_user):
        return self.role_repo.get_permissions()
    
    def update_role(self, role_id: UUID, role_in: RoleCreate, current_user):
        
        db_role = self.role_repo.get_by_id(role_id, current_user.tenant_id)
        
        update_data = role_in.model_dump(exclude_unset=True)
        
        if not update_data: return db_role
        
        if "name" in update_data:    
            role_exists = self.role_repo.get_by_name(update_data["name"], current_user.tenant_id)
            
            if role_exists:
                raise HTTPException(    
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This role already exists"
                )
        if "permissions" in update_data:
            permissions_data = self.role_repo.get_permissions()
            permissions = []
            for item in permissions_data:
                permissions.append(item.id)
            
            for permission in update_data["permissions"]:
                if permission not in permissions: 
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Permissions not valid"
                    )

        return self.role_repo.update(db_role, update_data)
    
    def delete_role(self, role_id: UUID, current_user):
        db_role = self.role_repo.get_by_id(role_id, current_user.tenant_id)
        
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )
        
        data = {"deleted_at": datetime.now(timezone.utc)}
        
        self.role_repo.update(db_role, data)
        return
    
    