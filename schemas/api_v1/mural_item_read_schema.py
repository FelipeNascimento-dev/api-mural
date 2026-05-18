from typing import Optional
import datetime
from pydantic import BaseModel, Field, field_serializer
from zoneinfo import ZoneInfo


class MuralItemReadBaseSC(BaseModel):
    mural_item_id: int
    user_id: int
    # is_read: bool


class MuralItemReadCreateSC(MuralItemReadBaseSC):
    pass


class MuralItemReadUpdateSC(MuralItemReadBaseSC):
    read_at: Optional[datetime.datetime] = None


class MuralItemReadInDbBaseSC(MuralItemReadBaseSC):
    id: int
    read_at: Optional[datetime.datetime]

    @field_serializer("read_at", when_used="json")
    def serialize_dt(self, dt: datetime.datetime | None):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        return dt.astimezone(ZoneInfo("America/Sao_Paulo")).isoformat()


class MuralItemReadByIdResponseSC(BaseModel):
    mural_item_id: int
    user_id: int
    read_at: Optional[datetime.datetime]
    username: str
    user_name: str
