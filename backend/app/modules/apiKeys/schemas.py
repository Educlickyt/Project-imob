from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiKeyCreate(BaseModel):
    name: str
    expires_at: datetime | None = None
    
class ApiKeyResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    key_prefix: str
    is_active: bool
    created_at: datetime
    expires_at: datetime | None = None
    
class ApiKeyCreatedResponse(BaseModel):
    id: UUID
    name: str
    key: str
    key_prefix: str
    message: str
