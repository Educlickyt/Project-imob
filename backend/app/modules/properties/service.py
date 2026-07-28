from datetime import datetime
import uuid
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, UploadFile

from app.core.storage import S3Storage
from app.modules.auth.schemas import TokenPayload
from app.modules.properties.models import Property
from app.modules.properties.repository import PropertyRepository
from app.modules.properties.schemas import PropertyCreate, PropertyUpdate, PropertyMediaResponse
from app.modules.users.repository import UserRepository
from app.workers.image_processor import process_image


class PropertyService:

    def __init__(self, db):
        self.property_repo = PropertyRepository(db)
        self.user_repo = UserRepository(db)

    def list_properties(self, current_user: TokenPayload):
        properties = self.property_repo.get_property(
            current_user.tenant_id, None
        )
        if not properties:
            raise HTTPException(
                status_code=404, detail="Properties not found"
            )
        return properties

    def get_property_by_id(self, property_id: UUID, current_user: TokenPayload):
        return self._get_property_or_404(property_id, current_user.tenant_id)

    def create_property(self, property_in: PropertyCreate, current_user: TokenPayload):
        user = self.user_repo.get_by_id(str(property_in.user_id), current_user.tenant_id)
        if not user:
            raise HTTPException(
                status_code=422, detail="User not found."
            )

        property_data = property_in.model_dump()
        property_data["tenant_id"] = current_user.tenant_id

        type_prefix = property_data["property_type"].upper()[:3]
        seq = self.property_repo.next_sequence(
            property_data["tenant_id"], type_prefix
        )
        property_data["slug"] = f"{type_prefix}{seq:04d}"

        property_data["status"] = self._check_status(property_data)

        return self.property_repo.create_property(property_data)

    def update_property(self, property_id: UUID, property_in: PropertyUpdate, current_user: TokenPayload):
        db_property = self._get_property_or_404(property_id, current_user.tenant_id)

        update_data = property_in.model_dump(exclude_unset=True)

        if "user_id" in update_data:
            if update_data["user_id"] is None:
                raise HTTPException(
                    status_code=422, detail="user_id cannot be null"
                )
            user = self.user_repo.get_by_id(str(update_data["user_id"]), current_user.tenant_id)
            if not user:
                raise HTTPException(
                    status_code=422, detail="User not found."
                )

        if not update_data:
            return db_property

        merged = {
            c.name: getattr(db_property, c.name)
            for c in Property.__table__.columns
        }
        merged.update(update_data)
        update_data["status"] = self._check_status(merged)
        
        if "publication_status" in update_data and update_data["publication_status"] != 'inactive':
            if update_data['status'] != 'registed': update_data.pop("publication_status", None)

        return self.property_repo.update_property(db_property, update_data)

    def _check_status(self, data: dict) -> str:
        important_fields = [
            "owner_id",
            "property_type",
            "transaction_type",
            "area",
            "address",
            "district",
            "city",
            "state",
            "zip_code",
        ]

        if data.get("property_type") == "APT":
            important_fields.extend([
                "iptu", "iptu_type", "condominium_fee",
                "bedrooms", "bathrooms", "garage_spots",
            ])
        elif data.get("property_type") == "CAS":
            important_fields.extend([
                "iptu", "iptu_type",
                "bedrooms", "bathrooms", "garage_spots",
            ])

        if data.get("transaction_type") == "rent":
            important_fields.append("price_rent")
        elif data.get("transaction_type") == "sale":
            important_fields.append("price_sale")

        for field in important_fields:
            value = data.get(field)
            if value is None or value == "" or value == 0:
                return "register incomplete"

        return "registed"

    def _get_property_or_404(self, property_id: UUID, tenant_id: UUID) -> Property:
        db_property = self.property_repo.get_by_id(property_id)
        if not db_property or db_property.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Property not found")
        return db_property

    def delete_property(self, property_id: UUID, current_user: TokenPayload):
        db_property = self._get_property_or_404(property_id, current_user.tenant_id)
        self.property_repo.update_property(db_property, {"deleted_at": datetime.utcnow()})

    def upload_media(
        self, property_id: UUID, file: UploadFile, background_tasks: BackgroundTasks, current_user: TokenPayload
    ) -> PropertyMediaResponse:
        self._get_property_or_404(property_id, current_user.tenant_id)

        file_bytes = file.file.read()
        media_id = uuid.uuid4()
        content_type = file.content_type or "image/jpeg"

        result = process_image(file_bytes, media_id, property_id, content_type)

        position = self.property_repo.get_next_position(property_id)
        is_cover = position == 0

        media_data = {
            "id": media_id,
            "property_id": property_id,
            "url": result["url"],
            "type": content_type,
            "position": position,
            "is_cover": is_cover,
        }
        db_media = self.property_repo.create_media(media_data)
        return PropertyMediaResponse.model_validate(db_media)

    def delete_media(self, media_id: UUID, current_user: TokenPayload):
        db_media = self.property_repo.get_media_by_id(media_id)
        if not db_media:
            raise HTTPException(status_code=404, detail="Media not found")

        self._get_property_or_404(db_media.property_id, current_user.tenant_id)

        base_key = f"properties/{db_media.property_id}/{media_id}"
        storage = S3Storage()
        for suffix in ("original.jpg", "large.jpg", "medium.jpg", "small.jpg"):
            storage.delete_file(f"{base_key}/{suffix}")

        self.property_repo.delete_media(db_media)

    def set_cover(self, property_id: UUID, media_id: UUID, current_user: TokenPayload):
        self._get_property_or_404(property_id, current_user.tenant_id)

        db_media = self.property_repo.get_media_by_id(media_id)
        if not db_media or db_media.property_id != property_id:
            raise HTTPException(status_code=404, detail="Media not found")

        medias = self.property_repo.get_medias_by_property(property_id)
        for m in medias:
            if m.is_cover:
                self.property_repo.update_media(m, {"is_cover": False})

        self.property_repo.update_media(db_media, {"is_cover": True})
        return PropertyMediaResponse.model_validate(db_media)
        