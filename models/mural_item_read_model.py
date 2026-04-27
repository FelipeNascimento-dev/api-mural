from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, UniqueConstraint
from db.base_class import Base


class MuralItemReadModel(Base):
    __tablename__ = "mural_item_read"
    __table_args__ = (
        UniqueConstraint("mural_item_id", "user_id",
                         name="uq_mural_item_read_user"),
    )

    id = Column(Integer, primary_key=True, index=True)

    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    is_read = Column(Boolean, nullable=False, default=False)
    read_at = Column(DateTime, nullable=True)
