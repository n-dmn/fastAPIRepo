from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_keyvault, get_db
from api.models.item import Item, ItemSchema
from core.keyvault import KeyVault

router = APIRouter()

@router.get("/items", response_model=List[ItemSchema])
def read_items(
    db: Session = Depends(get_db), vault: KeyVault = Depends(get_keyvault)
):
    if not db.query(Item).first():
        db_item = Item(name="foo", description=vault.get("API_KEY"))
        db.add(db_item)
        db.commit()
    return db.query(Item).all()
