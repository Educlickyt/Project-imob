import enum


class LeadStatus(str, enum.Enum):
    NEW = "new"
    ATTENDED = "Attended"
    DISCARDED = "Discarded"
