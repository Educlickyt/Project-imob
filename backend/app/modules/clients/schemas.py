from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ClientResponse(BaseModel):
    id: UUID = Field(...)
    tenant_id: UUID = Field(...)
    user_id: UUID = Field(...)
    create_from_lead_id: UUID | None = None
    name: str
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    
class ClientCreate(BaseModel):
    name: str = Field(...)
    user_id: UUID = Field(...)
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    
class ClientUpdate(BaseModel):
    name: str | None = None
    user_id: UUID | None = None
    email: str | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None
    