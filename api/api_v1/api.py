from fastapi import APIRouter

from api.api_v1.endpoints import (
    mural_item,
    mural_item_gai,
    mural_item_user,
    mural_item_group,
    mural_item_read,
    mural_item_v2
)

api_router = APIRouter()

api_router.include_router(mural_item.router,
                          prefix="/v1/items", tags=["items"])
api_router.include_router(mural_item_gai.router,
                          prefix="/v1/item-gais", tags=["item-gais"])
api_router.include_router(mural_item_user.router,
                          prefix="/v1/item-users", tags=["item-users"])
api_router.include_router(mural_item_group.router,
                          prefix="/v1/item-groups", tags=["item-groups"])
api_router.include_router(mural_item_read.router,
                          prefix="/v1/item-reads", tags=["item-reads"])
api_router.include_router(mural_item_v2.router,
                          prefix="/v2/items", tags=["items-v2"])
