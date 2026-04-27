

from crud.baseAsync import CRUDBase
from models.mural_item_user_model import MuralItemUserModel
from schemas.api_v1.mural_item_user_schema import MuralItemUserCreateSC, MuralItemUserUpdateSC


class CrudMuralItemUser(CRUDBase[MuralItemUserModel, MuralItemUserCreateSC, MuralItemUserUpdateSC]):
    pass


mural_item_user_crud = CrudMuralItemUser(MuralItemUserModel)
