from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.leads.schemas import LeadResponse, LeadUpdate
from app.modules.leads.service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/", response_model=List[LeadResponse])
def list(
    status: str | None = Query(None),
    property_id: UUID | None = Query(None),
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("leads:view")),
):
    service = LeadService(db)
    return service.list_leads(current_user.tenant_id, status, property_id)


@router.get("/{lead_id}", response_model=LeadResponse)
def get(
    lead_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("leads:view")),
):
    service = LeadService(db)
    return service.get_lead(lead_id, current_user.tenant_id)


@router.patch("/{lead_id}", response_model=LeadResponse)
def update(
    lead_id: UUID,
    data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("leads:update")),
):
    service = LeadService(db)
    return service.update_lead(lead_id, data.model_dump(exclude_unset=True), current_user.tenant_id)
