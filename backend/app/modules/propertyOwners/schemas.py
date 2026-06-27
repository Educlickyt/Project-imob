from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class PropertyOwnerCreate(BaseModel):
    name: str = Field(...)
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    
class PropertyOwnerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    
class PropertyOwnerResponse(BaseModel):
    id: UUID = Field(...)
    tenant_id: UUID = Field(...)
    name: str = Field(...)
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
