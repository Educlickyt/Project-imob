from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: UUID
    tenant_id: UUID
    roles: List[str]
    permissions: List[str]
    exp: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=25)
    name: str
    phone: str
    is_active: bool = Field(default=True)


class RegisterRequest(UserCreate):
    tenant_name: str
    tenant_slug: str | None = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    phone:str
    is_active: bool

    class Config:
        from_attributes = True

class TenantResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    plan: str
    status: str

    class Config:
        from_attributes = True