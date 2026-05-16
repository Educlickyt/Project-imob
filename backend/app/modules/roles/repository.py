from app.modules.roles.models import Role, RolePermission

class RoleRepository:
    
    def __init__(self, db):
        self.db = db
        
    def create(self, role_data: dict):
        
        db_role = Role(
            name = role_data['name'],
            description=role_data['description'],
            tenant_id=role_data['tenant_id']
        )
        self.db.add(db_role)
        
        self.db.flush()
        
        for perm in role_data['permissions']:
            role_permission = RolePermission(
                role_id= db_role.id,
                permission_id= perm
            )
            self.db.add(role_permission)
        
        self.db.commit()
        self.db.refresh(db_role)
    
        return db_role
    
    def get_by_name(self, name: str, tenant_id: str):
        from uuid import UUID 
        return self.db.query(Role).filter(Role.name == name and Role.tenant_id == UUID(tenant_id)).first()