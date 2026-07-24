import enum


class PortalType(str, enum.Enum):
    OLX = "olx"
    DREAMCASA = "dreamcasa"


class SyncStatus(str, enum.Enum):
    PENDING = "pending"
    SYNCED = "synced"
    FAILED = "failed"
    REMOVED = "removed"
