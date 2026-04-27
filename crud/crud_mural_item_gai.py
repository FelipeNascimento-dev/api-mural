

from crud.baseAsync import CRUDBase
from models.mural_item_gai_model import MuralItemGaiModel
from schemas.api_v1.mural_item_gai_schema import MuralItemGaiCreateSC, MuralItemGaiUpdateSC


class CrudMuralItemGAI(CRUDBase[MuralItemGaiModel, MuralItemGaiCreateSC, MuralItemGaiUpdateSC]):
    pass


mural_item_gai_crud = CrudMuralItemGAI(MuralItemGaiModel)
