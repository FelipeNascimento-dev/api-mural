from typing import Optional
from pydantic import BaseModel, Field


class MuralItemGroupBaseSC(BaseModel):
    mural_item_id: int
    gai_id: int


class MuralItemGroupCreateSC(MuralItemGroupBaseSC):
    pass


class MuralItemGroupUpdateSC(MuralItemGroupBaseSC):
    pass


class MuralItemGroupInDbBaseSC(MuralItemGroupBaseSC):
    id: int
