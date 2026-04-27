from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BigInteger, DateTime, Text, func
from sqlalchemy.orm import relationship
from db.base_class import Base
from models.auth_user_model import AuthUserModel


class MuralItemModel(Base):
    __tablename__ = "mural_item"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    summary = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)

    item_type = Column(String(30), nullable=False)
    severity = Column(String(20), nullable=False, default="informational")
    target_type = Column(String(20), nullable=False, default="all")

    is_active = Column(Boolean, nullable=False, default=True)
    is_pinned = Column(Boolean, nullable=False, default=False)

    starts_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),  # ✅ Python
        server_default=func.now(),
        nullable=False
    )
    ends_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    is_indefinite = Column(Boolean, nullable=False, default=False)
    until_read = Column(Boolean, nullable=False, default=False)

    external_link = Column(String(500), nullable=True)
    attachment_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)

    created_by_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    created_by = relationship("AuthUserModel", lazy="selectin")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
