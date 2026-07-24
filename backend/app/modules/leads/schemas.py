from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class LeadResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID | None = None
    property_id: UUID | None = None
    name: str
    email: str
    phone: str
    message: str
    status: str
    source: str
    raw_data: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadUpdate(BaseModel):
    status: str | None = None
    user_id: UUID | None = None
