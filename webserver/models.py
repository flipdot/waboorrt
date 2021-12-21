from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    rc3_identity = Column(String, primary_key=True, index=True)
    ssh_public_key = Column(String)
    repository = relationship("Repository", back_populates="owner", uselist=False)


class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True, index=True)
    owner = relationship("User", back_populates="repository", uselist=False)
