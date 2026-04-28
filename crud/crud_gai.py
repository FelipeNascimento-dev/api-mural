
from crud.baseAsync import CRUDBase


from models.gai_model import GaiModel
from schemas.api_v1.gai_schema import GaiCreateSC, GaiUpdateSC


class CrudMuralItem(CRUDBase[GaiModel, GaiCreateSC, GaiUpdateSC]):
    pass


gai_crud = CrudMuralItem(GaiModel)
