import uuid

from sqlalchemy import String, Text, Integer, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

from app.modules.propertyOwners.models import PropertyOwner  
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("property_owners.id"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(Text, nullable=True)

    property_type: Mapped[str] = mapped_column(String, nullable=True)

    transaction_type: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(String)

    publication_status: Mapped[str] = mapped_column(String, default="inactive")

    price_sale: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    price_rent: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    condominium_fee: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    iptu: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    iptu_type: Mapped[str] = mapped_column(String, nullable=True)
    
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=True)

    bathrooms: Mapped[int] = mapped_column(Integer,nullable=True)

    garage_spots: Mapped[int] = mapped_column(Integer, nullable=True)

    area: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    address: Mapped[str] = mapped_column(String,nullable=True)

    district: Mapped[str] = mapped_column(String,nullable=True)

    city: Mapped[str] = mapped_column(String, nullable=True)

    state: Mapped[str] = mapped_column(String, nullable=True)

    zip_code: Mapped[str] = mapped_column(String, nullable=True)



    views_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

class PropertyMedia(Base):
    __tablename__ = "property_medias"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    property_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("properties.id"),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    type: Mapped[str] = mapped_column(String)

    position: Mapped[int] = mapped_column(Integer)

    is_cover: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    