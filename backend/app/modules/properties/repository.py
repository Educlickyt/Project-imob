from uuid import UUID

from app.modules.properties.models import Property, PropertySequence, PropertyMedia


class PropertyRepository:

    def __init__(self, db):
        self.db = db

    def create_property(self, property_data: dict) -> Property:
        db_property = Property(**property_data)
        self.db.add(db_property)
        self.db.commit()
        self.db.refresh(db_property)
        return db_property

    def get_property(self, tenant_id: UUID, property_id: str | None = None):
        query = self.db.query(Property).filter(
            Property.tenant_id == tenant_id,
            Property.deleted_at.is_(None),
        )
        if property_id:
            return query.filter(Property.id == property_id).first()
        return query.all()

    def get_by_id(self, property_id: UUID) -> Property | None:
        return self.db.query(Property).filter(Property.id == property_id, Property.deleted_at.is_(None)).first()

    def next_sequence(self, tenant_id: UUID, property_type: str) -> int:
        seq = self.db.query(PropertySequence).filter(
            PropertySequence.tenant_id == tenant_id,
            PropertySequence.property_type == property_type,
        ).with_for_update().first()

        if not seq:
            seq = PropertySequence(
                tenant_id=tenant_id,
                property_type=property_type,
                last_sequence=1,
            )
            self.db.add(seq)
            self.db.flush()
            return 1

        seq.last_sequence += 1
        self.db.flush()
        return seq.last_sequence

    def update_property(self, db_property: Property, update_data: dict) -> Property:
        for key, value in update_data.items():
            setattr(db_property, key, value)
        self.db.commit()
        self.db.refresh(db_property)
        return db_property

    def create_media(self, media_data: dict) -> PropertyMedia:
        db_media = PropertyMedia(**media_data)
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def get_medias_by_property(self, property_id: UUID) -> list[PropertyMedia]:
        return self.db.query(PropertyMedia).filter(
            PropertyMedia.property_id == property_id
        ).order_by(PropertyMedia.position).all()

    def get_media_by_id(self, media_id: UUID) -> PropertyMedia | None:
        return self.db.query(PropertyMedia).filter(PropertyMedia.id == media_id).first()

    def delete_media(self, db_media: PropertyMedia):
        self.db.delete(db_media)
        self.db.commit()

    def update_media(self, db_media: PropertyMedia, update_data: dict) -> PropertyMedia:
        for key, value in update_data.items():
            setattr(db_media, key, value)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def get_next_position(self, property_id: UUID) -> int:
        last = self.db.query(PropertyMedia).filter(
            PropertyMedia.property_id == property_id
        ).order_by(PropertyMedia.position.desc()).first()
        return (last.position + 1) if last else 0
        