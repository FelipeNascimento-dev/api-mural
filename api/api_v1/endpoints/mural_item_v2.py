from typing import Any, List, Literal
import logging
from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field

from core.request import RequestClient
from api import deps
from models import mural_item_read_model
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.api_v1.mural_item_schema import MuralItemBaseSC, MuralItemCreateSC, MuralItemUpdateSC, MuralItemInDbBaseSC, MuralSeverityEnum, PayloadMuralItemCreateSC, MuralItemDeleteSC
from schemas.api_v1.mural_item_user_schema import MuralItemUserBaseSC, MuralItemUserCreateSC, MuralItemUserUpdateSC, MuralItemUserInDbBaseSC
from schemas.api_v1.mural_item_gai_schema import MuralItemGaiBaseSC, MuralItemGaiCreateSC, MuralItemGaiUpdateSC, MuralItemGaiInDbBaseSC
from schemas.api_v1.mural_item_group_schema import MuralItemGroupBaseSC, MuralItemGroupCreateSC, MuralItemGroupUpdateSC, MuralItemGroupInDbBaseSC

from crud.crud_mural_item import mural_item_crud
from crud.crud_mural_item_user import mural_item_user_crud
from crud.crud_mural_item_gai import mural_item_gai_crud
from crud.crud_mural_item_group import mural_item_group_crud
from crud.crud_mural_item_read import mural_item_read_crud
from crud.crud_gai import gai_crud

from service.mural_item_service import mural_item_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/create-item/", response_model=MuralItemInDbBaseSC)
async def create_item(
        *,
        db: AsyncSession = Depends(deps.get_db_psql),
        item_in: PayloadMuralItemCreateSC,
) -> Any:
    """
## Legenda dos campos:
### `item_type`:
- notice
- announcement
- script
- manual


### `severity`:
- informational
- moderate
- important
- critical


### `target_type`:
- all
- users
- gais
- groups

### `ids`: 
-Deve conter uma lista de ids das entidades as quais o item será atrelado. Sejam elas usuários, grupos ou gais (somente permitido uma por vez)

    """
    # item_payload = item_in.model_dump()

    mural_item_service.build_validation_itens(
        item_data=item_in,
        ids=item_in.ids
    )

    if item_in.target_type != 'all':
        ids = item_in.ids
        item_data = item_in.model_dump(exclude={"ids"})
    else:
        item_data = item_in.model_dump()

    item_result = await mural_item_crud.create(db=db, obj_in=MuralItemCreateSC(**item_data))

    if item_in.target_type == 'users':
        for user_id in ids:
            item_user_data = MuralItemUserCreateSC(
                user_id=user_id,
                mural_item_id=item_result.id
            )
            await mural_item_user_crud.create(db=db, obj_in=item_user_data)

    if item_in.target_type == 'gais':
        for gai_id in ids:
            item_gai_data = MuralItemGaiCreateSC(
                gai_id=gai_id,
                mural_item_id=item_result.id
            )
            await mural_item_gai_crud.create(db=db, obj_in=item_gai_data)

    if item_in.target_type == 'groups':
        for group_id in ids:
            item_group_data = MuralItemGroupCreateSC(
                group_id=group_id,
                mural_item_id=item_result.id
            )
            await mural_item_group_crud.create(db=db, obj_in=item_group_data)

    return item_result
