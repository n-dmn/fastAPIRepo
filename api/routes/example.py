from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_keyvault
from api.models.item import Item, ItemSchema
from api.models.user import User
from core.keyvault import KeyVault

router = APIRouter()

@router.get("/items", response_model=List[ItemSchema])
def read_items(
    db: Session = Depends(get_db), vault: KeyVault = Depends(get_keyvault)
):
    user = db.query(User).first()
    if not user:
        user = User(username="alice")
        db.add(user)
        db.commit()
        db.refresh(user)

    if not db.query(Item).first():
        db_item = Item(
            name="foo",
            description=vault.get("API_KEY"),
            owner_id=user.id,
        )
        db.add(db_item)
        db.commit()

    return db.query(Item).all()
