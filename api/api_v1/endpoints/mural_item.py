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

from schemas.api_v1.mural_item_schema import MuralItemBaseSC, MuralItemCreateSC, MuralItemUpdateSC, MuralItemInDbBaseSC, MuralSeverityEnum, PayloadMuralItemCreateSC
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


@router.get("/", response_model=List[MuralItemInDbBaseSC])
async def read_items(
        db: AsyncSession = Depends(deps.get_db_psql),
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
        db: AsyncSession = Depends(deps.get_db_psql)
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
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_psql)
) -> Any:
    """
    Consulta os itens do mural disponíveis para um usuário.

    Regras:
    - Itens atribuídos diretamente ao usuário;
    - Itens atribuídos ao GAI do usuário;
    - Itens atribuídos ao grupo do usuário, com base no GAI;
    - Itens com target_type = all;
    - Apenas ativos;
    - Apenas dentro do período de exibição;
    - Se until_read=True, só exibe enquanto o usuário não tiver lido.
    """

    logger.info("Consultando itens do mural por usuário")

    filters_default = mural_item_service.build_default_filters(
        relation=True)
    # =====================================================
    # 1. Buscar o GAI para descobrir o grupo do usuário
    # =====================================================

    gai = await gai_crud.get(db=db, id=gai_id)

    if not gai:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GAI não encontrado."
        )

    group_id = getattr(gai, "group_id", None)

    if not group_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O GAI informado não possui grupo vinculado."
        )

    # =====================================================
    # 2. Buscar itens atribuídos diretamente ao usuário
    # =====================================================
    itens_users_filters = filters_default + [
        {
            "field": "user_id",
            "operator": "=",
            "value": user_id
        }
    ]
    itens_user = await mural_item_user_crud.get_multi_dynamic_filters(
        db=db,
        filters=itens_users_filters
    )

    itens_user_ids = [
        item.mural_item_id
        for item in itens_user
    ]

    # =====================================================
    # 3. Buscar itens atribuídos ao GAI
    # =====================================================
    itens_gai_filters = filters_default + [
        {
            "field": "gai_id",
            "operator": "=",
            "value": gai_id
        }
    ]
    itens_gai = await mural_item_gai_crud.get_multi_dynamic_filters(
        db=db,
        filters=itens_gai_filters
    )

    itens_gai_ids = [
        item.mural_item_id
        for item in itens_gai
    ]

    # =====================================================
    # 4. Buscar itens atribuídos ao grupo do GAI
    # =====================================================
    itens_group_filters = filters_default + [
        {
            "field": "group_id",
            "operator": "=",
            "value": group_id
        }
    ]
    itens_group = await mural_item_group_crud.get_multi_dynamic_filters(
        db=db,
        filters=itens_group_filters
    )

    itens_group_ids = [
        item.mural_item_id
        for item in itens_group
    ]

    # =====================================================
    # 5. Buscar itens já lidos pelo usuário
    # =====================================================
    itens_lidos_filters = filters_default + [
        {
            "field": "user_id",
            "operator": "=",
            "value": user_id
        },
        {
            "field": "mural_item.until_read",
            "operator": "=",
            "value": True
        }
    ]
    itens_lidos = await mural_item_read_crud.get_multi_dynamic_filters(
        db=db,
        filters=itens_lidos_filters
    )

    itens_lidos_ids = [
        item.mural_item_id
        for item in itens_lidos
    ]

    # =====================================================
    # 6. Montar regra de visibilidade
    # =====================================================
    visibility_conditions = [
        {
            "field": "target_type",
            "operator": "=",
            "value": "all"
        },

    ]

    if itens_user_ids:
        visibility_conditions.append(
            {
                "logic": "and",
                "conditions": [
                    {
                        "field": "target_type",
                        "operator": "=",
                        "value": "users"
                    },
                    {
                        "field": "id",
                        "operator": "in",
                        "value": itens_user_ids
                    }
                ]
            }
        )

    if itens_gai_ids:
        visibility_conditions.append(
            {
                "logic": "and",
                "conditions": [
                    {
                        "field": "target_type",
                        "operator": "=",
                        "value": "gais"
                    },
                    {
                        "field": "id",
                        "operator": "in",
                        "value": itens_gai_ids
                    }
                ]
            }
        )

    if itens_group_ids:
        visibility_conditions.append(
            {
                "logic": "and",
                "conditions": [
                    {
                        "field": "target_type",
                        "operator": "=",
                        "value": "groups"
                    },
                    {
                        "field": "id",
                        "operator": "in",
                        "value": itens_group_ids
                    }
                ]
            }
        )

    # =====================================================
    # 7. Consulta final dos itens do mural
    # =====================================================

    filters = [
        {
            "logic": "or",
            "conditions": visibility_conditions
        },
        {
            "logic": "or",
            "conditions": [
                {
                    "field": "until_read",
                    "operator": "=",
                    "value": False
                },
                {
                    "field": "id",
                    "operator": "notin",
                    "value": itens_lidos_ids
                }
            ]
        },

    ]
    filters.extend(mural_item_service.build_default_filters(
        relation=False))

    itens = await mural_item_crud.get_multi_dynamic_filters(
        db=db,
        filters=filters,
        order_by="is_pinned",
        order_direction="desc",
        offset=offset,
        limit=limit,
        force_order_id=True
    )

    return itens


@router.post("/", response_model=MuralItemInDbBaseSC)
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
        db: AsyncSession = Depends(deps.get_db_psql),
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
