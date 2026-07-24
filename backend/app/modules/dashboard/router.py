from fastapi import APIRouter, Depends
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from app.modules.auth.dependencies import PermissionChecker, TokenPayload

from app.modules.dashboard.service import DashboardService
from app.modules.dashboard.schemas import DashboardSummary 

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("dashboard:view"))
):
    service = DashboardService(db)
    return service.get_summary(current_user.tenant_id)