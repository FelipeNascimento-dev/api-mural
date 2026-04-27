from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.api_v1.mural_item_schema import MuralItemBaseSC, MuralItemCreateSC, MuralItemUpdateSC, MuralItemInDbBaseSC
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


@router.post("/", response_model=MuralItemInDbBaseSC)
async def create_item(
        *,
        db: Session = Depends(deps.get_db_psql),
        item_in: MuralItemCreateSC,
) -> Any:
    """
    Create new item.
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
