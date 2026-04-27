

from crud.baseAsync import CRUDBase

from models.mural_item_group_model import MuralItemGroupModel
from schemas.api_v1.mural_item_group_schema import MuralItemGroupCreateSC, MuralItemGroupUpdateSC


class CrudMuralItemGroup(CRUDBase[MuralItemGroupModel, MuralItemGroupCreateSC, MuralItemGroupUpdateSC]):
    pass


mural_item_group_crud = CrudMuralItemGroup(MuralItemGroupModel)
