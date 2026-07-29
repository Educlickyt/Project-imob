from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ShowcaseConfigResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ShowcaseConfigUpdate(BaseModel):
    template: str | None = None
    is_active: bool | None = None
