
from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import relationship
from db.base_class import Base
from sqlalchemy.orm import declarative_base


class GaiModel(Base):
    __tablename__ = "logistica_groupaditionalinformation"

    id = Column(Integer, primary_key=True, index=True)

    # Campos espelhando o Django GroupAditionalInformation
    nome = Column(String(100), nullable=True)
    cod_iata = Column(String(100), nullable=True, index=True)
    # sales_channel = Column(String(100), nullable=True, index=True)
    # deposito = Column(String(100), nullable=True, index=True)
    # cod_center = Column(String(10), nullable=True, index=True)
    # inscricao_estadual = Column(String(20), nullable=True, index=True)
    # cnpj = Column(String(20), nullable=True, index=True)
    # razao_social = Column(String(20), nullable=True, index=True)

    # logradouro = Column(String(255), nullable=True)
    # numero = Column(String(10), nullable=True)
    # complemento = Column(String(100), nullable=True)
    # bairro = Column(String(100), nullable=True)
    # cidade = Column(String(100), nullable=True, index=True)
    # codigo_ibge = Column(String(20), nullable=True, index=True)
    # # Mantive ambos (como no Django). Se forem redundantes, escolha um só.
    # # estado = Column("UF", String(2), nullable=True, index=True)
    # UF = Column("UF", String(1))
    # CEP = Column(String(10), nullable=True, index=True)

    # telefone1 = Column(String(15), nullable=True)
    # telefone2 = Column(String(15), nullable=True)
    # # tamanho comum p/ e-mail
    # email = Column(String(254), nullable=True, index=True)
    # responsavel = Column(String(100), nullable=True)
