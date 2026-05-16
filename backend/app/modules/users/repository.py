from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from app.modules.users.models import User, UserRole
from app.modules.roles.models import Role, RolePermission,Permission
from app.core.security import get_password_hash

class UserRepository:
     
    def __init__(self, db):
        self.db = db
        
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
        
    def get_by_id(self, id: str):
        from uuid import UUID
        return self.db.query(User).filter(User.id == UUID(id)).first()
    
    def get_user_roles(self, user_id: str):
       
        query = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .where(UserRole.deleted_at.is_(None))
            .where(Role.deleted_at.is_(None))
        )
        
        result = self.db.execute(query)
        return list(result.scalars().all())
    
    def get_user_permissions_keys(self, user_id: str) -> list[str]:
        
        query = (
            select(distinct(Permission.key))
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == user_id)
            .where(UserRole.deleted_at.is_(None))
            .where(RolePermission.deleted_at.is_(None))
        )
        
        result = self.db.execute(query)
        
        return list(result.scalars().all())


    def create(self, user_data: dict):    
        
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))
        
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user