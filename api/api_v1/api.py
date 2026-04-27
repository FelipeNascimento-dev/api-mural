from fastapi import APIRouter

from api.api_v1.endpoints import mural_item, mural_item_gai, mural_item_user, mural_item_group, mural_item_read

api_router = APIRouter()

api_router.include_router(mural_item.router, prefix="/items", tags=["items"])
api_router.include_router(mural_item_gai.router,
                          prefix="/item-gais", tags=["item-gais"])
api_router.include_router(mural_item_user.router,
                          prefix="/item-users", tags=["item-users"])
api_router.include_router(mural_item_group.router,
                          prefix="/item-groups", tags=["item-groups"])
api_router.include_router(mural_item_read.router,
                          prefix="/item-reads", tags=["item-reads"])
