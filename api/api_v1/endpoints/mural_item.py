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


@router.get("/by-user/", response_model=List[MuralItemInDbBaseSC])
async def read_items_by_user(
    user_id: int,
    gai_id: int,
    offset: int = 0,
    limit: int = None,
    db: AsyncSession = Depends(deps.get_db_psql),
    reads: bool = False
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
    if reads:
        itens_lidos_ids = []
    else:
        itens_lidos_filters = filters_default + [
            {
                "field": "user_id",
                "operator": "=",
                "value": user_id
            }
            # },
            # {
            #     "field": "mural_item.until_read",
            #     "operator": "=",
            #     "value": True
            # }
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
    visibility_conditions = []

    visibility_conditions.append(mural_item_service.build_visibility_conditions(
        target_type="all", ids=[]))

    if itens_user_ids:
        visibility_conditions.append(
            mural_item_service.build_visibility_conditions(
                target_type="users", ids=itens_user_ids)
        )

    if itens_gai_ids:
        visibility_conditions.append(
            mural_item_service.build_visibility_conditions(
                target_type="gais", ids=itens_gai_ids)
        )

    if itens_group_ids:
        visibility_conditions.append(
            mural_item_service.build_visibility_conditions(
                target_type="groups", ids=itens_group_ids)
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
                # {
                #     "field": "until_read",
                #     "operator": "=",
                #     "value": False
                # },
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


@router.get("/by-created-by/", response_model=List[MuralItemInDbBaseSC])
async def read_items_by_creator(
    created_by_id: int,
    db: AsyncSession = Depends(deps.get_db_psql),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Consulta os itens do mural criados por um usuário específico.
    """
    logger.info("Consultando itens do mural por usuário criador")

    filters = [
        {
            "field": "created_by_id",
            "operator": "=",
            "value": created_by_id
        }
    ]

    itens = await mural_item_crud.get_multi_dynamic_filters(
        db=db,
        filters=filters,
        order_by="created_at",
        order_direction="desc",
        offset=skip,
        limit=limit
    )

    return itens


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


@router.put(path="/update-item/{id}", response_model=MuralItemInDbBaseSC)
async def update_item(
    *,
    db: AsyncSession = Depends(deps.get_db_psql),
    id: int,
    item_in: MuralItemUpdateSC,
) -> Any:
    item = await mural_item_crud.get(db=db, id=id)

    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    item_data_atual = MuralItemBaseSC(
        title=item.title,
        summary=item.summary,
        content=item.content,
        item_type=item.item_type,
        severity=item.severity,
        target_type=item.target_type,
        is_active=item.is_active,
        is_pinned=item.is_pinned,
        starts_at=item.starts_at,
        ends_at=item.ends_at,
        is_indefinite=item.is_indefinite,
        until_read=item.until_read,
        external_link=item.external_link,
        attachments=item.attachments,
        image_url=item.image_url,
        created_by_id=item.created_by_id
    )

    # item_data_update = item_in.model_dump(exclude_unset=True)

    # item_data_validacao = {
    #     **item_data_atual.model_dump(),
    #     **item_data_update,
    # }

    target_type_final = item_in.target_type or item_data_atual.target_type

    ids_vinculados = []

    if target_type_final == "users":
        vinculos = await mural_item_user_crud.get_multi_dynamic_filters(
            db=db,
            filters=[
                {
                    "field": "mural_item_id",
                    "operator": "=",
                    "value": id
                }
            ]
        )

        ids_vinculados = [
            vinculo.user_id
            for vinculo in vinculos
        ]

    elif target_type_final == "gais":
        vinculos = await mural_item_gai_crud.get_multi_dynamic_filters(
            db=db,
            filters=[
                {
                    "field": "mural_item_id",
                    "operator": "=",
                    "value": id
                }
            ]
        )

        ids_vinculados = [
            vinculo.gai_id
            for vinculo in vinculos
        ]

    elif target_type_final == "groups":
        vinculos = await mural_item_group_crud.get_multi_dynamic_filters(
            db=db,
            filters=[
                {
                    "field": "mural_item_id",
                    "operator": "=",
                    "value": id
                }
            ]
        )

        ids_vinculados = [
            vinculo.group_id
            for vinculo in vinculos
        ]

    mural_item_service.build_validation_itens(
        item_data=item_in,
        ids=ids_vinculados
    )

    item_updated = await mural_item_crud.update(
        db=db,
        db_obj=item,
        obj_in=item_in
    )

    return item_updated


@router.delete(path="/disable-item/{id}", response_model=MuralItemInDbBaseSC)
async def delete_item(
        *,
        db: AsyncSession = Depends(deps.get_db_psql),
        id: int
) -> Any:
    """
    Desabilita a visualização do item, sem remover o registro dele no DB.
    """
    item = await mural_item_crud.get(db=db, id=id)

    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    item_update = MuralItemDeleteSC(
        is_active=False
    )

    item_att = await mural_item_crud.update(db=db, db_obj=item, obj_in=item_update)
    return item_att
