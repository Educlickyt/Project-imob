from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class RoleCreate(BaseModel):
    name: str = Field(...)
    permissions: List[UUID]
    description: str
    
class RoleUpdate(BaseModel):
    name: str | None = None
    permissions: List[UUID] | None = None
    description: str | None = None
    
class RoleCreateResponse(BaseModel):
    id: UUID
    name: str = Field(...)
    # permissions: List[UUID]
    description: str
    
class RoleResponse(BaseModel):
    id: UUID 
    name: str
    description: str
    permissions: List[str]

class PermissionsResponse(BaseModel):
    id: UUID
    key: str
    description: str | None = None
    