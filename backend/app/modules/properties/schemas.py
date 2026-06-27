from pydantic import BaseModel, Field
from uuid import UUID
from typing import List
from datetime import datetime


class PropertyMediaResponse(BaseModel):
    id: UUID
    property_id: UUID
    url: str
    type: str
    position: int
    is_cover: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class PropertyResponse(BaseModel):
    id: UUID = Field(...)
    tenant_id: UUID = Field(...)
    user_id: UUID = Field(...)
    owner_id: UUID | None = None
    title: str
    slug: str | None = None
    description: str | None = None
    property_type: str | None = None
    transaction_type: str | None = None
    price_sale: float | None = None
    price_rent: float | None = None
    condominium_fee: float | None = None
    iptu: float | None = None
    iptu_type: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    garage_spots: int | None = None
    area: int | None = None
    address: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None

    status: str | None = None
    publication_status: str | None = None
    
    medias: List[PropertyMediaResponse] = []
    
    deleted_at: datetime | None = None
    
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
    
class PropertyCreate(BaseModel):
    user_id: UUID = Field(...) 
    owner_id: UUID | None = None
    title: str
    description: str | None = None
    property_type: str
    transaction_type: str | None = None
    price_sale: float | None = None
    price_rent: float | None = None
    condominium_fee: float | None = None
    iptu: float | None = None
    iptu_type: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    garage_spots: int | None = None
    area: int | None = None
    address: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    
class PropertyUpdate(BaseModel):
    user_id: UUID | None = None
    owner_id: UUID | None = None
    title: str | None = None
    description: str | None = None
    transaction_type: str | None = None
    price_sale: float | None = None
    price_rent: float | None = None
    condominium_fee: float | None = None
    iptu: float | None = None
    iptu_type: str | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    garage_spots: int | None = None
    area: int | None = None
    address: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    publication_status: str | None = None
    
