from sqlalchemy import Column, ForeignKey, Integer
from db.base_class import Base
from sqlalchemy.orm import relationship
from models.gai_model import GaiModel


class MuralItemDesignationModel(Base):
    __tablename__ = "logistica_userdesignation"

    id = Column(Integer, primary_key=True, index=True)
    gai_id = Column(Integer, ForeignKey("gai.id"), nullable=False,
                    index=True, name='informacao_adicional_id')
    # gai = relationship("GaiModel", lazy="selectin")
    user_id = Column(Integer, ForeignKey("auth_user.id"),
                     nullable=False, index=True)
