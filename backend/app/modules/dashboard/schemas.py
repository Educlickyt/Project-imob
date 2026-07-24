from pydantic import BaseModel, Field

class LeadsByStatus(BaseModel):
    new: int = 0
    Attended: int = 0
    Discarded: int = 0
    
class PropertiesByStatus(BaseModel):
    registed: int = 0
    register_incomplete: int = 0
    
class DashboardSummary(BaseModel):
    total_properties: int = 0
    total_leads: int = 0
    total_clients: int = 0
    leads_by_status: LeadsByStatus
    properties_by_status: PropertiesByStatus