from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository
from app.modules.roles.service import RoleService
from app.modules.users.schemas import UserCreate
from uuid import UUID

from datetime import datetime, timezone

class UserService:
     
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.role_service = RoleService(db)
 
    def create_user(self, user_in: UserCreate, tenant_id: UUID):
        user_exists = self.user_repo.get_by_email(user_in.email)
         
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esse email já está cadastrado."
            )
        
        user_data = user_in.model_dump()
        user_data['tenant_id'] = tenant_id
        
        return self.user_repo.create(user_data)
    
    def list_users(self, current_user):
        users = self.user_repo.get_users(current_user.tenant_id)
        
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found."
            )
        
        return users
    
    def get_user(self, user_id, current_user):
        user = self.user_repo.get_by_id(user_id, current_user.tenant_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        return user
    
    def update(self, user_id, user_in, current_user):
        
        db_user = self.user_repo.get_by_id(user_id, current_user.tenant_id)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        update_data = user_in.model_dump(exclude_unset=True)
        
        if not update_data: return db_user 
        
        if "roles" in update_data:
            db_roles = self.role_service.list_roles(current_user)
            
            role_ids = []
            for role in db_roles:
                role_ids.append(role.id)
            
            for role_id in update_data["roles"]:
                if role_id not in role_ids:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Roles not valid."
                    )
                    
        if "email" in update_data:
            user_exists = self.user_repo.get_by_email(update_data["email"])
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already in use."
                )
        
        
        return self.user_repo.update(db_user, update_data)
    
    def delete_user(self, user_id, current_user):
        db_user = self.user_repo.get_by_id(user_id, current_user.tenant_id)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        data = {"deleted_at": datetime.now(timezone.utc)}
        
        self.user_repo.update(db_user, data)
        return
    
        