from sqlalchemy import Column, ForeignKey, Integer
from db.base_class import Base


class MuralItemUserModel(Base):
    __tablename__ = "mural_item_user"

    id = Column(Integer, primary_key=True, index=True)
    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
