from typing import List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from fastapi.responses import Response

from app.core.dependencies import get_db
from app.core.storage import S3Storage
from app.modules.auth.dependencies import PermissionChecker, TokenPayload
from app.modules.properties.schemas import PropertyCreate, PropertyUpdate, PropertyMediaResponse, PropertyResponse
from app.modules.properties.service import PropertyService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=List[PropertyResponse])
def list(db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:view"))):
    property_service = PropertyService(db)
    return property_service.list_properties(current_user)

@router.get("/{property_id}", response_model=PropertyResponse)
def get(property_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:view"))):
    property_service = PropertyService(db)
    return property_service.get_property_by_id(property_id, current_user)

@router.post("/create")
def create(property_data: PropertyCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:create"))):
    
    property_service = PropertyService(db)
    return property_service.create_property(property_data, current_user)

@router.delete("/{property_id}", status_code=204)
def delete(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("properties:delete")),
):
    service = PropertyService(db)
    service.delete_property(property_id, current_user)

@router.patch("/{property_id}", response_model=PropertyResponse)
def update(property_id: UUID, property_data: PropertyUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:update"))):
    property_service = PropertyService(db)
    return property_service.update_property(property_id, property_data, current_user)

@router.get("/{property_id}/media", response_model=List[PropertyMediaResponse])
def list_media(property_id: UUID, db: Session = Depends(get_db), current_user: TokenPayload = Depends(PermissionChecker("properties:view"))):
    service = PropertyService(db)
    service._get_property_or_404(property_id, current_user.tenant_id)
    return service.property_repo.get_medias_by_property(property_id)

@router.post("/{property_id}/media", response_model=PropertyMediaResponse, status_code=201)
def upload_media(
    property_id: UUID,
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("properties:update")),
):
    service = PropertyService(db)
    return service.upload_media(property_id, file, background_tasks, current_user)

@router.delete("/{property_id}/media/{media_id}", status_code=204)
def delete_media(
    media_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("properties:update")),
):
    service = PropertyService(db)
    service.delete_media(media_id, current_user)

@router.patch("/{property_id}/media/{media_id}/cover", response_model=PropertyMediaResponse)
def set_cover(
    property_id: UUID,
    media_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(PermissionChecker("properties:update")),
):
    service = PropertyService(db)
    return service.set_cover(property_id, media_id, current_user)


media_router = APIRouter(prefix="/media", tags=["media"])

@media_router.get("/{media_id}")
def serve_media(media_id: UUID, db: Session = Depends(get_db)):
    from app.modules.properties.repository import PropertyRepository
    repo = PropertyRepository(db)
    db_media = repo.get_media_by_id(media_id)
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")
    storage = S3Storage()
    data = storage.get_file(db_media.url)
    if data is None:
        raise HTTPException(status_code=404, detail="File not found in storage")
    return Response(content=data, media_type=db_media.type)