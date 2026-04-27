from typing import Optional, Text, List
from pydantic import BaseModel, Field
from datetime import datetime


class MuralItemBaseSC(BaseModel):
    title: str
    summary: str
    content: Text

    item_type: str
    severity: str
    target_type: str
    is_active: bool
    is_pinned: bool

    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    is_indefinite: bool
    until_read: bool

    external_link: str
    attachment_url: str
    image_url: str

    created_by: int


class MuralItemCreateSC(MuralItemBaseSC):
    pass


class MuralItemUpdateSC(MuralItemBaseSC):
    updated_at: Optional[datetime] = None


class MuralItemInDbBaseSC(MuralItemBaseSC):
    id: int
