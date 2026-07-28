from datetime import datetime, timezone

from app.modules.apiKeys.models import ApiKey

class ApiKeyRepository:
    
    def __init__(self, db):
        self.db = db
        
    def create(self, apikey_data: dict) -> ApiKey:
        db_key = ApiKey(**apikey_data)
        self.db.add(db_key)
        self.db.commit()
        self.db.refresh(db_key)
        return db_key
    
    def get_keys(self, tenant_id) -> list[ApiKey]:
        return self.db.query(ApiKey).filter(ApiKey.tenant_id == tenant_id, ApiKey.is_active == True).all()
        
    def get_by_id(self, key_id, tenant_id) -> ApiKey | None:
        return self.db.query(ApiKey).filter(ApiKey.tenant_id == tenant_id, ApiKey.id == key_id).first()
    
    def update(self, db_key: ApiKey, update_data: dict) -> ApiKey:
        for key, value in update_data.items():
            setattr(db_key, key, value)
        self.db.commit()
        self.db.refresh(db_key)
        return db_key

    def delete(self, db_key: ApiKey):
        self.db.delete(db_key)
        self.db.commit()
