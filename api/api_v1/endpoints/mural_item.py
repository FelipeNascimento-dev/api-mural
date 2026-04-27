from typing import Any, List, Literal
import logging
from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.api_v1.mural_item_schema import MuralItemBaseSC, MuralItemCreateSC, MuralItemUpdateSC, MuralItemInDbBaseSC, MuralSeverityEnum
from crud.crud_mural_item import mural_item_crud
from api import deps

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
    # filters = [
    #     {
    #         "field": "last_in_movement.origin.stock_type",
    #         "operator": "=",
    #         "value": stock_type
    #     }
    # ]

    item = await mural_item_crud.get_multi_filters(
        db=db, )
    return item


@router.post("/", response_model=MuralItemInDbBaseSC)
async def create_item(
        *,
        db: Session = Depends(deps.get_db_psql),
        item_in: MuralItemCreateSC,
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

    """
    item = await mural_item_crud.create(db=db, obj_in=item_in)
    return item


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
