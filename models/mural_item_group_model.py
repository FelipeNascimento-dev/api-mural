from db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.auth_group_model import AuthGroupModel  # noqa


class MuralItemGroupModel(Base):
    __tablename__ = "mural_item_group"

    id = Column(Integer, primary_key=True, index=True)
    mural_item = relationship("MuralItemModel", lazy="selectin")
    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("auth_group.id"), nullable=False)
