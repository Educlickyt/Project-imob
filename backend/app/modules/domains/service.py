import secrets
from datetime import datetime, timezone

from fastapi import HTTPException

from app.modules.domains.models import TenantDomain
from app.modules.domains.repository import DomainRepository
from app.modules.domains.schemas import DomainCreate


class DomainService:
    def __init__(self, db):
        self.domain_repo = DomainRepository(db)

    def create(self, domain_in: DomainCreate, current_user) -> TenantDomain:
        
        # Verifica se o domínio já está cadastrado por outro corretor
        existing = self.domain_repo.get_by_domain(domain_in.domain)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Domain already registered"
            )

        # Gera token de verificação
        verification_token = secrets.token_urlsafe(32)

        # Monta os dados
        domain_data = {
            "tenant_id": current_user.tenant_id,
            "domain": domain_in.domain,
            "is_primary": domain_in.is_primary,
            "verified": False,           # Começa como não verificado
            "ssl_active": False,         # SSL post-MVP
            "verification_token": verification_token,
        }

        return self.domain_repo.create(domain_data)

    def list_domains(self, current_user) -> list[TenantDomain]:
        return self.domain_repo.get_domains(current_user.tenant_id)

    def get_domain(self, domain_id, current_user) -> TenantDomain:
        db_domain = self.domain_repo.get_by_id(domain_id, current_user.tenant_id)
        
        if not db_domain:
            raise HTTPException(status_code=404, detail="Domain not found")
        
        return db_domain

    def delete(self, domain_id, current_user):
        db_domain = self.get_domain(domain_id, current_user)
        self.domain_repo.delete(db_domain)