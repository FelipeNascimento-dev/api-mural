from typing import Any, List, Optional
import logging

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session

from schemas.api_v1.mural_item_read_schema import MuralItemReadBaseSC, MuralItemReadCreateSC, MuralItemReadByIdResponseSC, MuralItemReadInDbBaseSC
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


@router.get("/by-user/{user_id}", response_model=List[MuralItemReadInDbBaseSC])
async def read_item_reads_by_user(
        user_id: int,
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve item_reads by user_id.
    """
    logger.info(f"Consultando leituras dos itens do usuário {user_id}")

    return await mural_item_read_crud.get_multi_dynamic_filters(
        db=db,
        filters=[
            {
                "field": "user_id",
                "operator": "==",
                "value": user_id,
            }
        ],
        order_by="read_at",
        order_direction="desc",
        offset=skip,
        limit=limit,
    )


@router.get("/by-item-id/{item_id}", response_model=List[MuralItemReadByIdResponseSC])
async def read_item_read_by_id(
        item_id: int,
        db: Session = Depends(deps.get_db_psql),
        skip: int = 0,
        limit: int = 20,
        username: Optional[str] = None,
        name: Optional[str] = None,
        gai_id: Optional[int] = None
) -> Any:
    """
    Retrieve an item_read by its ID.
    """
    logger.info(f"Consultando leitura do item com ID {item_id}")

    filters = [
        {
            "field": "mural_item_id",
            "operator": "==",
            "value": item_id,
        }
    ]

    if username:
        filters.append({
            "field": "user.username",
            "operator": "==",
            "value": username,
        })

    if name:
        filters.append({
            "logic": "or",
            "conditions": [
                {
                    "field": "user.first_name",
                    "operator": "ilike",
                    "value": f"%{name}%",
                },
                {
                    "field": "user.last_name",
                    "operator": "ilike",
                    "value": f"%{name}%",
                }
            ]
        })

    if gai_id:
        filters.append({
            "field": "user.designation.gai_id",
            "operator": "==",
            "value": gai_id,
        })

    items = await mural_item_read_crud.get_multi_dynamic_filters(
        db=db,
        filters=filters,
        order_by="read_at",
        order_direction="desc",
        offset=skip,
        limit=limit,
    )

    items_response = [MuralItemReadByIdResponseSC(
        mural_item_id=item.mural_item_id,
        user_id=item.user_id,
        read_at=item.read_at,
        username=item.user.username,
        user_name=item.user.first_name.strip() + " " + item.user.last_name.strip()
    ) for item in items]

    return items_response


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
