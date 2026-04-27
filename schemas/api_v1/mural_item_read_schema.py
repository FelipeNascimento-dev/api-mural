from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MuralItemReadBaseSC(BaseModel):
    mural_item_id: int
    user_id: int
    is_read: bool


class MuralItemReadCreateSC(MuralItemReadBaseSC):
    pass


class MuralItemReadUpdateSC(MuralItemReadBaseSC):
    read_at: Optional[datetime] = None


class MuralItemReadInDbBaseSC(MuralItemReadBaseSC):
    id: int
