from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

# class Token(BaseModel):
#     access_token: str
#     token_type: str = "bearer"

# class TokenPayload(BaseModel):
#     sub: str = None  # user_id
#     exp: int = None

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str
    
class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=25)
    name: str
    phone: str
    is_active: bool = Field(default=True)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    phone:str
    is_active: bool

    class Config:
        from_attributes = True