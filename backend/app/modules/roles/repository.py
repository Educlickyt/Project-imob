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
    
    def get_admin_role(self):
        return self.db.query(Role).filter(Role.name == 'admin', Role.tenant_id == None).first()
    
    def get_by_name(self, name: str, tenant_id: str):
        return self.db.query(Role).filter(Role.name == name, Role.tenant_id == tenant_id).first()