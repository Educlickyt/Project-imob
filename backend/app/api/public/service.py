from fastapi import HTTPException

from app.api.public.repository import PublicRepository

class PublicService:
    def __init__(self, db):
        self.public_repo = PublicRepository(db)

    def list_properties(self, tenant_id, filters):
        properties, total = self.public_repo.get_published_properties(tenant_id, **filters)
        
        # Calcula paginação
        page = filters.get("page", 1)
        page_size = filters.get("page_size", 12)
        total_pages = (total + page_size - 1) // page_size
        
        # Retorna dict simples — Pydantic converte automaticamente
        return {
            "data": properties,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
            }
        }

    def get_property(self, property_id, tenant_id):
        property = self.public_repo.get_property_by_id(property_id, tenant_id)
        
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        if property.publication_status != "active":
            raise HTTPException(status_code=404, detail="Property not found")
        
        return property 

    def get_tenant_info(self, tenant_id):
        tenant = self.public_repo.get_tenant_by_id(tenant_id)

        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        from app.modules.showcaseConfigs.service import ShowcaseConfigService
        showcase_service = ShowcaseConfigService(self.public_repo.db)
        showcase_config = showcase_service.get_config_for_public(tenant_id)

        # Busca dados de contato do admin do tenant
        from app.modules.users.models import User, UserRole
        from app.modules.roles.models import Role

        admin_user = (
            self.public_repo.db.query(User)
            .join(UserRole, UserRole.user_id == User.id)
            .join(Role, Role.id == UserRole.role_id)
            .filter(
                User.tenant_id == tenant_id,
                Role.name == "admin",
                User.is_active == True,
            )
            .first()
        )

        return {
            "name": tenant.name,
            "slug": tenant.slug,
            "phone": admin_user.phone if admin_user else None,
            "email": admin_user.email if admin_user else None,
            "showcase": showcase_config,
        }  

    def create_contact(self, tenant_id, contact_in, request_data):
        if not contact_in.email:
            raise HTTPException(status_code=422, detail="Email is required")
        
        lead = self.public_repo.create_lead(
            tenant_id=tenant_id,
            name=contact_in.name,
            email=contact_in.email,
            phone=contact_in.phone,
            message=contact_in.message,
            property_id=contact_in.property_id,
            raw_data=request_data,
        )
        
        return {"message": "Contact sent successfully"}