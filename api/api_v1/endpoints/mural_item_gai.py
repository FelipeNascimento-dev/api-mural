from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.api_v1.mural_item_gai_schema import MuralItemGaiBaseSC, MuralItemGaiCreateSC, MuralItemGaiUpdateSC, MuralItemGaiInDbBaseSC
from crud.crud_mural_item_gai import mural_item_gai_crud
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[MuralItemGaiInDbBaseSC])
async def read_item_gais(
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve item_gais.
    """
    logger.info("Consultando GAIs do item")
    return await mural_item_gai_crud.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=MuralItemGaiInDbBaseSC)
async def create_item_gai(
        *,
        db: Session = Depends(deps.get_db_psql),
        item_gai_in: MuralItemGaiCreateSC,
) -> Any:
    """
    Create new item_gai.
    """
    item_gai = await mural_item_gai_crud.create(db=db, obj_in=item_gai_in)
    return item_gai


@router.delete(path="/{id}", response_model=MuralItemGaiInDbBaseSC)
async def delete_item_gai(
        *,
        db: Session = Depends(deps.get_db_psql),
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item_gai = await mural_item_gai_crud.get(db=db, id=id)
    if not item_gai:
        raise HTTPException(status_code=404, detail="item_gai not found")
    item_gai = await mural_item_gai_crud.remove(db=db, id=id)
    return item_gai
