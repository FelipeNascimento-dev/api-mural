from typing import Optional
from pydantic import BaseModel, Field


class MuralItemGaiBaseSC(BaseModel):
    mural_item_id: int
    gai_id: int


class MuralItemGaiCreateSC(MuralItemGaiBaseSC):
    pass


class MuralItemGaiUpdateSC(MuralItemGaiBaseSC):
    pass


class MuralItemGaiInDbBaseSC(MuralItemGaiBaseSC):
    id: int
