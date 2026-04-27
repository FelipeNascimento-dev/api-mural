from typing import Optional
from pydantic import BaseModel, Field


class AuthUserBaseSC(BaseModel):
    username: str
    is_superuser: bool
    is_staff: bool


class AuthUserCreateSC(AuthUserBaseSC):
    pass


class AuthUserUpdateSC(AuthUserBaseSC):
    pass


class AuthUserInDbBaseSC(AuthUserBaseSC):
    id: int
