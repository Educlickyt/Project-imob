from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.showcaseConfigs.schemas import ShowcaseConfigResponse, ShowcaseConfigUpdate
from app.modules.showcaseConfigs.service import ShowcaseConfigService

router = APIRouter(prefix="/showcase-config", tags=["showcase-config"])


@router.get("/", response_model=ShowcaseConfigResponse)
def get_config(
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("showcase-config:view"))
):
    service = ShowcaseConfigService(db)
    return service.get_config(current_user.tenant_id)


@router.patch("/", response_model=ShowcaseConfigResponse)
def update_config(
    config_in: ShowcaseConfigUpdate,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("showcase-config:update"))
):
    service = ShowcaseConfigService(db)
    return service.update_config(current_user.tenant_id, config_in)
