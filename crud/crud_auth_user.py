from crud.baseAsync import CRUDBase
from models.auth_user_model import AuthUserModel
from schemas.api_v1.auth_user_schema import AuthUserCreateSC, AuthUserUpdateSC


class CRUDItem(CRUDBase[AuthUserModel, AuthUserCreateSC, AuthUserUpdateSC]):
    pass


auth_user_crud = CRUDItem(AuthUserModel)
