from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.api_v1.mural_item_read_schema import MuralItemReadBaseSC, MuralItemReadCreateSC, MuralItemReadUpdateSC, MuralItemReadInDbBaseSC
from crud.crud_mural_item_read import mural_item_read_crud
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[MuralItemReadInDbBaseSC])
async def read_item_reads(
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve item_reads.
    """
    logger.info("Consultando Leituras dos itens")
    return await mural_item_read_crud.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=MuralItemReadInDbBaseSC)
async def create_item_read(
        *,
        db: Session = Depends(deps.get_db_psql),
        item_read_in: MuralItemReadCreateSC,
) -> Any:
    """
    Create new item_read.
    """
    item_read = await mural_item_read_crud.create(db=db, obj_in=item_read_in)
    return item_read


@router.delete(path="/{id}", response_model=MuralItemReadInDbBaseSC)
async def delete_item_read(
        *,
        db: Session = Depends(deps.get_db_psql),
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item_read = await mural_item_read_crud.get(db=db, id=id)
    if not item_read:
        raise HTTPException(status_code=404, detail="item_read not found")
    item_read = await mural_item_read_crud.remove(db=db, id=id)
    return item_read
