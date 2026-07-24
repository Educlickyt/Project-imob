from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from app.core.dependencies import get_db
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from sqlalchemy.orm import Session

from app.modules.clients.schemas import ClientResponse, ClientCreate, ClientUpdate
from app.modules.clients.service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post('/create', response_model=ClientResponse)
def create(client_data: ClientCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("clients:create"))):
    service = ClientService(db)
    return service.create(current_user, client_data)

@router.get('/', response_model=List[ClientResponse])
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("clients:view"))):
    service = ClientService(db)
    return service.list(current_user)

@router.get('/{client_id}', response_model=ClientResponse)
def get(client_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("clients:view"))):
    service = ClientService(db)
    return service.get(current_user, client_id)

@router.patch('/{client_id}', response_model=ClientResponse)
def update(client_id: UUID, client_data: ClientUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("clients:update"))):
    service = ClientService(db)
    return service.update(current_user, client_id, client_data)

@router.delete('/{client_id}', status_code=204)
def delete(client_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("clients:delete"))):
    service = ClientService(db)
    return service.delete(current_user, client_id)
