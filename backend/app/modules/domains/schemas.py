from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DomainCreate(BaseModel):
    domain: str
    is_primary: bool = True
    

class DomainResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    domain: str
    is_primary: bool
    verified: bool
    ssl_active: bool
    created_at: datetime
    updated_at: datetime