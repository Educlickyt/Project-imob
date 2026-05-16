from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class RoleCreate(BaseModel):
    name: str = Field(...)
    permissions: List[UUID]
    description: str
    
class RoleResponse(BaseModel):
    id: UUID 
    name: str
    description: str