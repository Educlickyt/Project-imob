from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.domains.schemas import DomainCreate, DomainResponse
from app.modules.domains.service import DomainService

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("/", response_model=List[DomainResponse])
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = DomainService(db)
    return service.list_domains(current_user)


@router.get("/{domain_id}", response_model=DomainResponse)
def get(domain_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:view"))):
    service = DomainService(db)
    return service.get_domain(domain_id, current_user)


@router.post("/create", response_model=DomainResponse, status_code=201)
def create(domain_in: DomainCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:create"))):
    service = DomainService(db)
    return service.create(domain_in, current_user)


@router.delete("/{domain_id}", status_code=204)
def delete(domain_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("roles:delete"))):
    service = DomainService(db)
    service.delete(domain_id, current_user)