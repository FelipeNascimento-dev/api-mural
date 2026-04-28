from typing import Optional
from pydantic import BaseModel


# Se já tiver o Enum no seu módulo de modelos, importe-o:
# from .models import GaiType


class GaiBaseSC(BaseModel):
    nome: Optional[str] = None
    cod_iata: Optional[str] = None
    group_id: int
    # Pydantic v2
    model_config = {"from_attributes": True, "use_enum_values": True}
    # Se estiver em Pydantic v1, use:
    # class Config:
    #     orm_mode = True
    #     use_enum_values = True


class GaiCreateSC(GaiBaseSC):
    pass


class GaiUpdateSC(GaiBaseSC):
    pass  # se quiser "PATCH estrito", mantenha todos opcionais aqui


class GaiInDbBaseSC(GaiBaseSC):
    id: int


class Gai(GaiInDbBaseSC):
    pass
