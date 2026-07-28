import secrets
import hashlib
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modules.apiKeys.repository import ApiKeyRepository

class ApiKeyService:
    
    def __init__(self, db):
        self.apikey_repo = ApiKeyRepository(db)
        
    def generate_apikey(self) -> str:
        random_part = secrets.token_urlsafe(32) #32 bytes aleatórios
        return f"sk_live_{random_part}"
    
    def hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()
    
    def get_prefix(self, key: str) -> str:
        return key[:16]
    
    def create(self, key_in: dict, current_user) -> dict:
        key = self.generate_apikey()
        
        key_hash = self.hash_key(key)
        
        key_prefix = self.get_prefix(key)
        
        apikey_data ={
            "tenant_id": current_user.tenant_id,
            "name": key_in.name,
            "key_hash": key_hash,
            "key_prefix": key_prefix,
            "is_active": True,
            "expires_at": key_in.expires_at
        }
        
        db_key = self.apikey_repo.create(apikey_data)
        
        return {
            "id": db_key.id,
            "name": db_key.name,
            "key": key,
            "key_prefix": key_prefix,
            "message": "Guarde essa chave. Ela não será mostrada novamente"
        }
        
    def list_keys(self, current_user) -> list[dict]:
        db_keys = self.apikey_repo.get_keys(current_user.tenant_id)
        
        if not db_keys:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No key found."
            )
        
        return db_keys
    
    def get_key(self, key_id, current_user) -> dict:
        db_key = self.apikey_repo.get_by_id(key_id, current_user.tenant_id)
        
        if not db_key:
            raise HTTPException(status_code=404, detail="API Key not found")
        
        return db_key

    def toggle_active(self, key_id, current_user) -> dict:
        db_key = self.get_key(key_id, current_user)
        
        new_status = not db_key.is_active 
        return self.apikey_repo.update(db_key, {"is_active": new_status})
    
    def delete(self, key_id, current_user):
        db_key = self.get_key(key_id, current_user)
        self.apikey_repo.delete(db_key)

        
        
