from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from db.base_class import Base


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

    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=True)

    is_indefinite = Column(Boolean, nullable=False, default=False)
    until_read = Column(Boolean, nullable=False, default=False)

    external_link = Column(String(500), nullable=True)
    attachment_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)

    created_by = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
