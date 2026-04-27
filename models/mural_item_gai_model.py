from sqlalchemy import Column, ForeignKey, Integer
from db.base_class import Base
from sqlalchemy.orm import relationship
from models.gai_model import GaiModel


class MuralItemGaiModel(Base):
    __tablename__ = "mural_item_gai"

    id = Column(Integer, primary_key=True, index=True)
    mural_item = relationship("MuralItemModel", lazy="selectin")
    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    gai_id = Column(Integer, ForeignKey(
        "logistica_groupaditionalinformation.id"), nullable=False, index=True)
