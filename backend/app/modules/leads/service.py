from uuid import UUID

from fastapi import HTTPException

from app.modules.leads.repository import LeadRepository
from app.modules.properties.repository import PropertyRepository
from app.modules.users.repository import UserRepository


class LeadService:

    def __init__(self, db):
        self.repo = LeadRepository(db)
        self.property_repo = PropertyRepository(db)
        self.user_repo = UserRepository(db)

    def list_leads(self, tenant_id: UUID, status: str | None = None, property_id: UUID | None = None):
        return self.repo.get_many(tenant_id, status, property_id)

    def get_lead(self, lead_id: UUID, tenant_id: UUID):
        lead = self.repo.get_by_id(lead_id)
        if not lead or lead.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Lead not found")
        return lead

    def create_lead(self, data: dict, tenant_id: UUID):
        data["tenant_id"] = tenant_id
        return self.repo.create(data)

    def update_lead(self, lead_id: UUID, update_data: dict, tenant_id: UUID):
        lead = self.repo.get_by_id(lead_id)
        if not lead or lead.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        if "user_id" in update_data and update_data["user_id"] is not None:
            user = self.user_repo.get_by_id(str(update_data["user_id"]), tenant_id)
            if not user:
                raise HTTPException(status_code=422, detail="User not found.")

        return self.repo.update(lead, update_data)
