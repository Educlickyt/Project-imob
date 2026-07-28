import uuid

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

from app.core.database import Base


class TenantDomain(Base):
    __tablename__ = "tenant_domains"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), 
        nullable=False
    )
    
    domain: Mapped[str] = mapped_column(
        Text, 
        nullable=False, 
        unique=True
    )
    
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    ssl_active: Mapped[bool] = mapped_column(Boolean, default=False)
    
    verification_token: Mapped[str] = mapped_column(Text, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc))