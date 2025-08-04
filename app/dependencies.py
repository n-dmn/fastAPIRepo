from typing import Optional

from .services.keyvault import KeyVault


_keyvault: Optional[KeyVault] = None


def get_keyvault() -> KeyVault:
    assert _keyvault is not None, "KeyVault not initialized"
    return _keyvault


def set_keyvault(kv: KeyVault) -> None:
    global _keyvault
    _keyvault = kv
