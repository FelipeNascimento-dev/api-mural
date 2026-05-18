from sqlalchemy import Boolean, Column, DateTime, Integer, String
from db.base_class import Base
from sqlalchemy.orm import relationship
from models.mural_item_designation_model import MuralItemDesignationModel


class AuthUserModel(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    # password = Column(String, nullable=False)
    # last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    username = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False, default="")
    last_name = Column(String, nullable=False, default="")
    # email = Column(String, nullable=False, default="", index=True)
    is_staff = Column(Boolean, nullable=False, default=False)
    # is_active = Column(Boolean, nullable=False, default=True)
    # date_joined = Column(DateTime, nullable=False)
    designation = relationship(
        "MuralItemDesignationModel", lazy="selectin")
