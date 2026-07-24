from app.modules.roles.models import Role, RolePermission, Permission
from sqlalchemy import select, distinct, and_
from datetime import datetime, timezone

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
        return self.db.query(Role).filter(Role.name == name, Role.tenant_id == tenant_id, Role.deleted_at.is_(None)).first()
    
    def get_by_id_with_permissions(self, id: str, tenant_id: str):
        role_rows = (
            self.db.query(Role.id, Role.name, Role.description, Permission.key)
            .outerjoin(RolePermission, and_(
                RolePermission.role_id == Role.id,
                RolePermission.deleted_at.is_(None)      # ← aqui
            ))
            .outerjoin(Permission, Permission.id == RolePermission.permission_id)
            .filter(Role.id == id, Role.tenant_id == tenant_id, Role.deleted_at.is_(None))
            .all()
        )    
        return role_rows
    
    def get_roles(self, tenant_id: str):        
        rows = (
            self.db.query(Role.id, Role.name, Role.description, Permission.key)
            .outerjoin(RolePermission, and_(
                RolePermission.role_id == Role.id,
                RolePermission.deleted_at.is_(None)
            ))
            .outerjoin(Permission, Permission.id == RolePermission.permission_id)
            .filter(Role.tenant_id == tenant_id, Role.deleted_at.is_(None))
            .all()
        )
        return rows
    
    def get_permissions(self):
        return self.db.query(Permission).all()
        
    def get_by_id(self, id: str, tenant_id: str) -> Role:
        return self.db.query(Role).filter(Role.id == id, Role.tenant_id == tenant_id, Role.deleted_at.is_(None)).first()
        
    def update(self, db_role: Role, data: dict) -> Role:
        
        if "permissions" in data:
            permissions = data.pop("permissions")
            
            db_role_permissions_rows = self.db.query(RolePermission).filter(RolePermission.role_id == db_role.id, RolePermission.deleted_at.is_(None)).all()
            
            db_permissions_id = []
            for row in db_role_permissions_rows:
                db_permissions_id.append(row.permission_id)
                if row.permission_id not in permissions:
                    setattr(row, "deleted_at", datetime.now(timezone.utc))

            for perm_id in permissions:
                if perm_id not in db_permissions_id:
                    self.db.add(RolePermission(role_id=db_role.id,permission_id=perm_id))
                    
        for key, value in data.items():
            setattr(db_role, key, value)
            
        self.db.commit()
        self.db.refresh(db_role)
        
        return db_role
    