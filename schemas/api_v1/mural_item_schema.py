import datetime
from pydantic import BaseModel, field_serializer
from typing import Optional, Text, Literal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from enum import Enum


class MuralTypeEnum(str, Enum):
    notice = "notice"
    announcement = "announcement"
    script = "script"
    manual = "manual"


class MuralSeverityEnum(str, Enum):
    informational = "informational"
    moderate = "moderate"
    important = "important"
    critical = "critical"


class MuralTargetTypeEnum(str, Enum):
    all = "all"
    users = "users"
    gais = "gais"
    groups = "groups"


class MuralItemBaseSC(BaseModel):
    title: str
    summary: str
    content: Text

    item_type: MuralTypeEnum
    severity: MuralSeverityEnum
    target_type: MuralTargetTypeEnum
    is_active: bool = True
    is_pinned: bool = False

    starts_at: Optional[datetime.datetime] = None
    ends_at: Optional[datetime.datetime] = None

    is_indefinite: bool = False
    until_read: bool = False

    external_link: str
    attachment_url: str
    image_url: str

    created_by_id: int

    @field_serializer("starts_at", "ends_at", when_used="json")
    def serialize_dt(self, dt: datetime.datetime | None):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        return dt.astimezone(ZoneInfo("America/Sao_Paulo")).isoformat()


class MuralItemCreateSC(MuralItemBaseSC):
    pass


class MuralItemUpdateSC(BaseModel):
    title: str
    summary: str
    content: Text

    item_type: MuralTypeEnum
    severity: MuralSeverityEnum
    target_type: MuralTargetTypeEnum
    is_active: bool = True
    is_pinned: bool = False

    starts_at: Optional[datetime.datetime] = None
    ends_at: Optional[datetime.datetime] = None

    is_indefinite: bool = False
    until_read: bool = False

    external_link: str
    attachment_url: str
    image_url: str

    created_by_id: int

    @field_serializer("starts_at", "ends_at", when_used="json")
    def serialize_dt(self, dt: datetime.datetime | None):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        return dt.astimezone(ZoneInfo("America/Sao_Paulo")).isoformat()


class MuralItemInDbBaseSC(MuralItemBaseSC):
    id: int


class PayloadMuralItemCreateSC(MuralItemCreateSC):
    ids: Optional[list[int]] = None
