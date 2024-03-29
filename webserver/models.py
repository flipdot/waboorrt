from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True, unique=True)
    username = Column(String, index=True, unique=True, nullable=False)
    rc3_identity = Column(String, index=True, unique=True, nullable=True)
    ssh_public_key = Column(String, unique=True)
    repository = relationship("RepositoryModel", back_populates="owner", uselist=False)
    is_superuser = Column(Boolean, default=False)


class RepositoryModel(Base):
    __tablename__ = "repositories"
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="repository", uselist=False)


class APIKeyModel(Base):
    __tablename__ = "api-keys"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True, unique=True)
