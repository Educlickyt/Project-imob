from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from app.modules.properties.models import Property, PropertyMedia
from app.modules.tenants.models import Tenant
from app.modules.leads.models import Lead


class PublicRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_published_properties(
        self,
        tenant_id: UUID,
        price_min: float = None,
        price_max: float = None,
        property_type: str = None,
        transaction_type: str = None,
        bedrooms: int = None,
        city: str = None,
        district: str = None,
        page: int = 1,
        page_size: int = 12,
    ) -> tuple[list[Property], int]:
        """
        Busca imóveis publicados de um tenant.
        
        Retorna tupla: (lista de imóveis, total de resultados)
        """
        # Filtros base (sem joinedload para count precisar)
        base_filters = [
            Property.tenant_id == tenant_id,
            Property.publication_status == "active",
            Property.deleted_at.is_(None),
        ]
        
        if price_min is not None:
            base_filters.append(Property.price_sale >= price_min)
        if price_max is not None:
            base_filters.append(Property.price_sale <= price_max)
        if property_type:
            base_filters.append(Property.property_type == property_type)
        if transaction_type:
            base_filters.append(Property.transaction_type == transaction_type)
        if bedrooms is not None:
            base_filters.append(Property.bedrooms == bedrooms)
        if city:
            base_filters.append(Property.city.ilike(f"%{city}%"))
        if district:
            base_filters.append(Property.district.ilike(f"%{district}%"))
        
        # Count sem joinedload (preciso)
        total = self.db.query(Property).filter(*base_filters).count()
        
        # Query com joinedload para buscar dados
        offset = (page - 1) * page_size
        properties = (
            self.db.query(Property)
            .options(joinedload(Property.medias))
            .filter(*base_filters)
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        return properties, total

    def get_property_by_id(self, property_id: UUID, tenant_id: UUID) -> Property | None:
        """Busca um imóvel específico (com mídias)."""
        return (
            self.db.query(Property)
            .options(joinedload(Property.medias))
            .filter(
                Property.id == property_id,
                Property.tenant_id == tenant_id,
                Property.deleted_at.is_(None),
            )
            .first()
        )

    def get_tenant_by_id(self, tenant_id: UUID) -> Tenant | None:
        """Busca dados do tenant."""
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def create_lead(
        self,
        tenant_id: UUID,
        name: str,
        email: str,
        phone: str = None,
        message: str = None,
        property_id: UUID = None,
        raw_data: dict = None,
    ) -> Lead:
        """Cria um lead a partir do formulário de contato."""
        lead = Lead(
            tenant_id=tenant_id,
            name=name,
            email=email,
            phone=phone,
            message=message or "",
            property_id=property_id,
            status="novo",
            source="vitrine",
            raw_data=raw_data or {},
        )
        
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        
        return lead