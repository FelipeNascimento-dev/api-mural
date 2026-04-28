from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, UniqueConstraint, func
from db.base_class import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class MuralItemReadModel(Base):
    __tablename__ = "mural_item_read"
    __table_args__ = (
        UniqueConstraint("mural_item_id", "user_id",
                         name="uq_mural_item_read_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    mural_item = relationship("MuralItemModel", lazy="selectin")
    mural_item_id = Column(Integer, ForeignKey(
        "mural_item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    # is_read = Column(Boolean, nullable=False, default=False)
    read_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),  # ✅ Python
        server_default=func.now(),
        nullable=False
    )
