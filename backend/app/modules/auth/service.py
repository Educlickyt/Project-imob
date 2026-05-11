from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository

class AuthService:
    
    def __init__(self, db):
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_in):
        
        user_exists = self.user_repo.get_by_email(user_in.email)
        
        # return user_exists
        
        
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esse email já está cadastrado."
            )
        
        return self.user_repo.create(user_in.model_dump())

    
    