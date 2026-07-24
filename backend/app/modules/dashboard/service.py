from app.modules.properties.models import Property
from app.modules.leads.models import Lead
from app.modules.clients.models import Client

from app.modules.dashboard.schemas import DashboardSummary, LeadsByStatus, PropertiesByStatus

from sqlalchemy import func


class DashboardService:
    
    def __init__(self, db):
        self.db = db
        
    def get_summary(self, tenant_id):
        # 1. Count properties (deleted_at IS NULL)
        total_properties = self.db.query(Property).filter(
            Property.tenant_id == tenant_id,
            Property.deleted_at.is_(None)
        ).count()
    
        # 2. Count leads
        total_leads = self.db.query(Lead).filter(
            Lead.tenant_id == tenant_id
        ).count()
        
        # 3. Count clients (deleted_at IS NULL)
        total_clients = self.db.query(Client).filter(
            Client.tenant_id == tenant_id,
            Client.deleted_at.is_(None)
        ).count()
        
        # 4. Group leads by status
        leads_by_status = self.db.query(
            Lead.status, func.count(Lead.id)
        ).filter(
            Lead.tenant_id == tenant_id
        ).group_by(Lead.status).all()
        
        # 5. Group properties by status
        properties_by_status = self.db.query(
            Property.status, func.count(Property.id)
        ).filter(
            Property.tenant_id == tenant_id,
            Property.deleted_at.is_(None)
        ).group_by(Property.status).all()
        
        leads_dict = {"new": 0, "Attended": 0, "Discarded": 0}
        for status, count in leads_by_status:
            if status in leads_dict:
                leads_dict[status] = count

        properties_dict = {"registed": 0, "register_incomplete": 0}
        for status, count in properties_by_status:
            if status == "register incomplete":
                properties_dict["register_incomplete"] = count
            elif status == "registed":
                properties_dict["registed"] = count

        return DashboardSummary(
            total_properties=total_properties,
            total_leads=total_leads,
            total_clients=total_clients,
            leads_by_status=LeadsByStatus(**leads_dict),
            properties_by_status=PropertiesByStatus(**properties_dict)
        )