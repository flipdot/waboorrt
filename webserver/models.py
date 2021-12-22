from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    rc3_identity = Column(String, index=True, unique=True, nullable=True)
    ssh_public_key = Column(String)
    repository = relationship("RepositoryModel", back_populates="owner", uselist=False)


class RepositoryModel(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="repository", uselist=False)
