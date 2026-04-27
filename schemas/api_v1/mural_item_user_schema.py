from typing import Optional
from pydantic import BaseModel, Field


class MuralItemUserBaseSC(BaseModel):
    mural_item_id: int
    user_id: int


class MuralItemUserCreateSC(MuralItemUserBaseSC):
    pass


class MuralItemUserUpdateSC(MuralItemUserBaseSC):
    pass


class MuralItemUserInDbBaseSC(MuralItemUserBaseSC):
    id: int
