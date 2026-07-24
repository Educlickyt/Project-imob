from uuid import UUID

from app.modules.leads.models import Lead


class LeadRepository:

    def __init__(self, db):
        self.db = db

    def get_many(self, tenant_id: UUID, status: str | None = None, property_id: UUID | None = None):
        query = self.db.query(Lead).filter(Lead.tenant_id == tenant_id)

        if status:
            query = query.filter(Lead.status == status)
        if property_id:
            query = query.filter(Lead.property_id == property_id)

        return query.order_by(Lead.created_at.desc()).all()

    def get_by_id(self, lead_id: UUID) -> Lead | None:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def create(self, data: dict) -> Lead:
        lead = Lead(**data)
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def update(self, db_lead: Lead, data: dict) -> Lead:
        for key, value in data.items():
            setattr(db_lead, key, value)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead
