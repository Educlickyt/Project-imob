from app.modules.auth.models import UserRefreshToken
from sqlalchemy import delete
from datetime import datetime

class AuthRepository:
    
    def __init__(self, db):
        self.db = db
        
    def save_refresh_token(self, user_id, token, expires_at: datetime):
        db_token = UserRefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        
        return db_token
    
    def get_refresh_token(self, token_str):
        return self.db.query(UserRefreshToken).filter(UserRefreshToken.token == token_str).first()

    def rotate_refresh_token(self, old_token: UserRefreshToken, new_token_str: str, expires_at):
        self.db.delete(old_token)
        
        new_token = UserRefreshToken(
            user_id=old_token.user_id,
            token=new_token_str,
            expires_at=expires_at
        )
        self.db.add(new_token)
        self.db.commit()
        
    def delete_refresh_token(self, token):
        self.db.delete(token)
        self.db.commit()
        
    def delete_all_user_tokens(self, user_id):
        stmt = delete(UserRefreshToken).where(
            UserRefreshToken.user_id == user_id
        )
        
        self.db.execute(stmt)
        self.db.commit()
        
        
    