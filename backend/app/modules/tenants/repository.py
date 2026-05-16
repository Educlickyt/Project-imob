from sqlalchemy.orm import Session
from app.modules.tenants.models import Tenant

class TenantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str):
        return self.db.query(Tenant).filter(Tenant.slug == slug).first()

    def get_by_id(self, id):
        return self.db.query(Tenant).filter(Tenant.id == id).first()
    
    def create(self, tenant_data: dict):
        db_tenant = Tenant(**tenant_data)
        self.db.add(db_tenant)
        self.db.commit()
        self.db.refresh(db_tenant)
        return db_tenant