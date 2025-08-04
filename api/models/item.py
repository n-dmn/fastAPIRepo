from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from core.database import Base, DB_SCHEMA


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(
        Integer,
        ForeignKey(f"{DB_SCHEMA}.users.id", name="fk_items_users_owner_id"),
        nullable=False,
    )
    owner = relationship("User", back_populates="items")


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int

    class Config:
        orm_mode = True
