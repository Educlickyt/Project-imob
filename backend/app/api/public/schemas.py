from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class PropertyMediaPublicResponse(BaseModel):
    """Mídia de um imóvel (versão pública — sem dados internos)."""
    id: UUID
    url: str
    type: str
    position: int
    is_cover: bool


class PropertyPublicResponse(BaseModel):
    """Imóvel listado na vitrine."""
    id: UUID
    title: str
    slug: str | None = None
    description: str | None = None
    property_type: str | None = None
    transaction_type: str | None = None
    price_sale: float | None = None
    price_rent: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    garage_spots: int | None = None
    area: float | None = None
    address: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    medias: List[PropertyMediaPublicResponse] = []
    created_at: datetime


class PaginationResponse(BaseModel):
    """Informações de paginação."""
    total: int
    page: int
    page_size: int
    total_pages: int


class PropertyListResponse(BaseModel):
    """Resposta da listagem de imóveis."""
    data: List[PropertyPublicResponse]
    pagination: PaginationResponse


class PropertyDetailResponse(PropertyPublicResponse):
    """Detalhe de um imóvel (mais campos que a listagem)."""
    views_count: int
    iptu: float | None = None
    condominium_fee: float | None = None


class ShowcasePublicInfo(BaseModel):
    """Dados públicos da configuração de vitrine."""
    template: str
    primary_color: str | None = None
    secondary_color: str | None = None


class TenantInfoResponse(BaseModel):
    """Dados públicos do corretor."""
    name: str
    slug: str
    slogan: str | None = None
    logo: str | None = None
    phone: str | None = None
    email: str | None = None
    showcase: ShowcasePublicInfo | None = None


class ContactCreate(BaseModel):
    """Campos do formulário de contato."""
    name: str
    email: str
    phone: str | None = None
    message: str | None = None
    property_id: UUID | None = None