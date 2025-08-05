from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base, DB_SCHEMA


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    items = relationship("Item", back_populates="owner")

