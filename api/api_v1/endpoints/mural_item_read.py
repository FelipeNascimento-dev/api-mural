from typing import Any, List
import logging

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session

from schemas.api_v1.mural_item_read_schema import MuralItemReadBaseSC, MuralItemReadCreateSC, MuralItemReadUpdateSC, MuralItemReadInDbBaseSC
from crud.crud_mural_item_read import mural_item_read_crud
from crud.crud_mural_item import mural_item_crud
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
        manualconfirmation: bool = False
) -> Any:
    """
    Create new item_read.
    """
    item_read = await mural_item_read_crud.get_last_by_filters(
        db=db,
        filters={
            "mural_item_id": {"operator": "==", "value": item_read_in.mural_item_id},
            "user_id": {"operator": "==", "value": item_read_in.user_id}
        }
    )
    if item_read:
        return item_read

    item = await mural_item_crud.get(db=db, id=item_read_in.mural_item_id)

    if item.until_read and not manualconfirmation:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Item possui confimação obrigatória!")

    try:
        item_read = await mural_item_read_crud.create(db=db, obj_in=item_read_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
