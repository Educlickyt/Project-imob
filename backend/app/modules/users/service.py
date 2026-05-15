from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate
from uuid import UUID

class UserService:
     
    def __init__(self, db):
        self.user_repo = UserRepository(db)
 
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