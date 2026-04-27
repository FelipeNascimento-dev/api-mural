from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.api_v1.mural_item_group_schema import MuralItemGroupBaseSC, MuralItemGroupCreateSC, MuralItemGroupUpdateSC, MuralItemGroupInDbBaseSC
from crud.crud_mural_item_group import mural_item_group_crud
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[MuralItemGroupInDbBaseSC])
async def read_item_groups(
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve item_groups.
    """
    logger.info("Consultando Grupos do item")
    return await mural_item_group_crud.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=MuralItemGroupInDbBaseSC)
async def create_item_group(
        *,
        db: Session = Depends(deps.get_db_psql),
        item_group_in: MuralItemGroupCreateSC,
) -> Any:
    """
    Create new item_group.
    """
    item_group = await mural_item_group_crud.create(db=db, obj_in=item_group_in)
    return item_group


@router.delete(path="/{id}", response_model=MuralItemGroupInDbBaseSC)
async def delete_item_group(
        *,
        db: Session = Depends(deps.get_db_psql),
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item_group = await mural_item_group_crud.get(db=db, id=id)
    if not item_group:
        raise HTTPException(status_code=404, detail="item_group not found")
    item_group = await mural_item_group_crud.remove(db=db, id=id)
    return item_group
