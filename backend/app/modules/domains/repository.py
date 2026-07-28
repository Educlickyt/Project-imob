import uuid
from datetime import datetime, timezone

from app.modules.domains.models import TenantDomain


class DomainRepository:
    def __init__(self, db):
        self.db = db

    def create(self, domain_data: dict) -> TenantDomain:
        db_domain = TenantDomain(**domain_data)
        self.db.add(db_domain)
        self.db.commit()
        self.db.refresh(db_domain)
        return db_domain

    def get_domains(self, tenant_id) -> list[TenantDomain]:
        return (
            self.db.query(TenantDomain)
            .filter(TenantDomain.tenant_id == tenant_id)
            .all()
        )

    def get_by_id(self, domain_id, tenant_id) -> TenantDomain | None:
        return (
            self.db.query(TenantDomain)
            .filter(
                TenantDomain.id == domain_id,
                TenantDomain.tenant_id == tenant_id
            )
            .first()
        )

    def get_by_domain(self, domain: str) -> TenantDomain | None:
        return (
            self.db.query(TenantDomain)
            .filter(TenantDomain.domain == domain)
            .first()
        )

    def update(self, db_domain: TenantDomain, update_data: dict) -> TenantDomain:
        for key, value in update_data.items():
            setattr(db_domain, key, value)
        self.db.commit()
        self.db.refresh(db_domain)
        return db_domain

    def delete(self, db_domain: TenantDomain):
        self.db.delete(db_domain)
        self.db.commit()