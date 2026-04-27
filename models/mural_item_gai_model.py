from sqlalchemy import Column, ForeignKey, Integer
from db.base_class import Base


class MuralItemGaiModel(Base):
    __tablename__ = "mural_item_gai"

    id = Column(Integer, primary_key=True, index=True)
    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    gai_id = Column(Integer, ForeignKey(
        "logistica_groupaditionalinformation.id"), nullable=False, index=True)
