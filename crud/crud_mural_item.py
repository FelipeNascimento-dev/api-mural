
from crud.baseAsync import CRUDBase


from models.mural_item_model import MuralItemModel
from schemas.api_v1.mural_item_schema import MuralItemCreateSC, MuralItemUpdateSC


class CrudMuralItem(CRUDBase[MuralItemModel, MuralItemCreateSC, MuralItemUpdateSC]):
    pass


mural_item_crud = CrudMuralItem(MuralItemModel)
