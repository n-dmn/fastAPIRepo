from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

from core.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True
