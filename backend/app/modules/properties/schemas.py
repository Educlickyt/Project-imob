from pydantic import BaseModel, Field
from uuid import UUID
from typing import List
from datetime import datetime


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

    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
    
class PropertyCreate(BaseModel):
    tenant_id: UUID = Field(default='6c7749f7-10d2-4ac4-809d-a2a659e3bf59') #teste
    user_id: UUID = Field(default='981d7a76-316f-42a9-a5bd-e7cee1119471') #teste
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
    
class PropertyUpdate(BaseModel):
    id: UUID = Field(...)
    tenant_id: UUID | None = None
    user_id: UUID | None = None
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
    
