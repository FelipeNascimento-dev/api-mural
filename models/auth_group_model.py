from sqlalchemy import Boolean, Column, DateTime, Integer, String
from db.base_class import Base


class AuthGroupModel(Base):
    __tablename__ = "auth_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="")
