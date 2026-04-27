from typing import Optional
from pydantic import BaseModel, Field


class AuthGroupBaseSC(BaseModel):
    name: str


class AuthGroupCreateSC(AuthGroupBaseSC):
    pass


class AuthGroupUpdateSC(AuthGroupBaseSC):
    pass


class AuthGroupInDbBaseSC(AuthGroupBaseSC):
    id: int
