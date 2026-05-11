from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.core.security import get_password_hash

class UserRepository:
    
    def __init__(self, db):
        self.db = db
        
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user_data: dict):    
        
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))

        user_data["tenant_id"] = "d3b3e3e3-e3e3-4e3e-a3e3-e3e3e3e3e3e3"
        print(user_data)
        
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user