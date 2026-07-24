from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import List


class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=25)
    name: str
    phone: str
    roles: List[UUID] 

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    phone: str
    is_active: bool
    tenant_id: UUID

    class Config:
        from_attributes = True
        

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    phone: str | None = None
    roles: List[UUID] | None = None
    is_active: bool | None = None
