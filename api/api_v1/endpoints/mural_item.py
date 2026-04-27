from typing import Any, List, Literal
import logging
from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
from sqlalchemy.orm import Session
from core.request import RequestClient
from api import deps

from schemas.api_v1.mural_item_schema import MuralItemBaseSC, MuralItemCreateSC, MuralItemUpdateSC, MuralItemInDbBaseSC, MuralSeverityEnum, PayloadMuralItemCreateSC
from schemas.api_v1.mural_item_user_schema import MuralItemUserBaseSC, MuralItemUserCreateSC, MuralItemUserUpdateSC, MuralItemUserInDbBaseSC
from schemas.api_v1.mural_item_gai_schema import MuralItemGaiBaseSC, MuralItemGaiCreateSC, MuralItemGaiUpdateSC, MuralItemGaiInDbBaseSC
from schemas.api_v1.mural_item_group_schema import MuralItemGroupBaseSC, MuralItemGroupCreateSC, MuralItemGroupUpdateSC, MuralItemGroupInDbBaseSC

from crud.crud_mural_item import mural_item_crud
from crud.crud_mural_item_user import mural_item_user_crud
from crud.crud_mural_item_gai import mural_item_gai_crud
from crud.crud_mural_item_group import mural_item_group_crud

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[MuralItemInDbBaseSC])
async def read_items(
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    logger.info("Consultando Itens")
    return await mural_item_crud.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{id}", response_model=MuralItemInDbBaseSC)
async def read_item_by_id(
        id: int,
        db: Session = Depends(deps.get_db_psql)
) -> Any:
    """
    Consulta um item pelo id
    """
    logger.info("Consultando Item")
    item = await mural_item_crud.get_first_by_filter(
        db=db, filterby="id", filter=id)
    return item


@router.get("/by-user/", response_model=List[MuralItemInDbBaseSC])
async def read_items_by_user(
        user_id: int,
        gai_id: int,
        # groups_ids: str = Query(
        # description="Ids dos grupos separados por pipe (|)"
        # ),
        db: Session = Depends(deps.get_db_psql)
) -> Any:
    """
    Consulta os itens com base no id do usuário de criação
    """
    logger.info("Consultando Itens")
    # groups_ids = groups_ids.split("|") if groups_ids else []
    filters_itens_user = [
        {
            "field": "user_id",
            "operator": "=",
            "value": user_id
        }
    ]

    itens_user = await mural_item_user_crud.get_multi_filters(
        db=db, filters=filters_itens_user)

    itens_ids = [item.mural_item_id for item in itens_user]

    item = await mural_item_crud.get_multi_filters(
        db=db, filters=[
            {
                "field": "id",
                "operator": "in",
                "value": itens_ids
            }
        ])

    return item


@router.post("/", response_model=MuralItemInDbBaseSC)
async def create_item(
        *,
        db: Session = Depends(deps.get_db_psql),
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
    if item_in.target_type != 'all' and not item_in.ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="O campo ids é obrigatório quando o target for 'all'")
    if item_in.target_type != 'all':
        ids = item_in.ids
        item_data = item_in.model_dump(exclude={"ids"})

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


@router.delete(path="/{id}", response_model=MuralItemInDbBaseSC)
async def delete_item(
        *,
        db: Session = Depends(deps.get_db_psql),
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item = await mural_item_crud.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    item = await mural_item_crud.remove(db=db, id=id)
    return item
