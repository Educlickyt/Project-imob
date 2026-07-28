from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.api.public.deps import get_tenant_from_request
from app.api.public.service import PublicService
from app.api.public.schemas import PropertyListResponse, PropertyDetailResponse, TenantInfoResponse, ContactCreate


router = APIRouter(prefix="/v1", tags=["public"])

@router.get("/{slug}/properties", response_model=PropertyListResponse)
def list_properties(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
    # Filtros opcionais via query params (?price_min=200000&bedrooms=3)
    price_min: float = None,
    price_max: float = None,
    property_type: str = None,
    transaction_type: str = None,
    bedrooms: int = None,
    city: str = None,
    district: str = None,
    page: int = 1,
    page_size: int = 12,
):
    """
    Lista imóveis publicados de um corretor.
    
    Exemplos:
    GET /v1/joao-silva/properties
    GET /v1/joao-silva/properties?price_min=200000&bedrooms=3
    GET /v1/joao-silva/properties?page=2&page_size=6
    """
    # 1. Resolve qual tenant está sendo acessado (slug ou domínio)
    tenant = get_tenant_from_request(request, slug)
    
    # 2. Monta dicionário de filtros
    filters = {
        "price_min": price_min,
        "price_max": price_max,
        "property_type": property_type,
        "transaction_type": transaction_type,
        "bedrooms": bedrooms,
        "city": city,
        "district": district,
        "page": page,
        "page_size": page_size,
    }
    
    # 3. Delega para o service (router não acessa o banco!)
    service = PublicService(db)
    return service.list_properties(tenant["tenant_id"], filters)


@router.get("/{slug}/properties/{property_id}", response_model=PropertyDetailResponse)
def get_property(
    slug: str,
    property_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Retorna detalhes de um imóvel específico.
    
    Exemplo:
    GET /v1/joao-silva/properties/uuid-do-imovel
    """
    tenant = get_tenant_from_request(request, slug)
    
    service = PublicService(db)
    return service.get_property(property_id, tenant["tenant_id"])


@router.get("/{slug}/info", response_model=TenantInfoResponse)
def get_tenant_info(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Retorna dados públicos do corretor/imobiliária.
    
    Exemplo:
    GET /v1/joao-silva/info
    """
    tenant = get_tenant_from_request(request, slug)
    
    service = PublicService(db)
    return service.get_tenant_info(tenant["tenant_id"])


@router.post("/{slug}/contact", status_code=201)
def create_contact(
    slug: str,
    contact_in: ContactCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Visitante preenche formulário → cria lead no ERP do corretor.
    """
    tenant = get_tenant_from_request(request, slug)
    
    # Coleta dados da requisição (para rastreamento)
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "")
    referrer = request.headers.get("referer", "")
    
    request_data = {
        "ip": ip_address,
        "user_agent": user_agent,
        "referrer": referrer,
    }
    
    service = PublicService(db)
    return service.create_contact(
        tenant["tenant_id"],
        contact_in,
        request_data
    )   