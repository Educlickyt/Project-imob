from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.core.security import get_password_hash

class UserRepository:
     
    def __init__(self, db):
        self.db = db
        
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
        
    def get_by_id(self, id: str):
        from uuid import UUID
        return self.db.query(User).filter(User.id == UUID(id)).first()
        
    def create(self, user_data: dict):    
        
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))
        
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user