from typing import Optional, Generator

from sqlalchemy.orm import Session

from core.keyvault import KeyVault
from core.database import SessionLocal

_keyvault: Optional[KeyVault] = None

def get_keyvault() -> KeyVault:
    assert _keyvault is not None, "KeyVault not initialized"
    return _keyvault


def set_keyvault(kv: KeyVault) -> None:
    global _keyvault
    _keyvault = kv


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
