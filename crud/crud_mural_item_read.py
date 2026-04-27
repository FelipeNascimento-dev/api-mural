

from crud.baseAsync import CRUDBase
from models.mural_item_read_model import MuralItemReadModel
from schemas.api_v1.mural_item_read_schema import MuralItemReadCreateSC, MuralItemReadUpdateSC


class CrudMuralItemRead(CRUDBase[MuralItemReadModel, MuralItemReadCreateSC, MuralItemReadUpdateSC]):
    pass


mural_item_read_crud = CrudMuralItemRead(MuralItemReadModel)
