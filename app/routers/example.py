from fastapi import APIRouter, Depends

from ..dependencies import get_keyvault
from ..services.keyvault import KeyVault

router = APIRouter()


@router.get("/items")
async def read_items(vault: KeyVault = Depends(get_keyvault)):
    return {"items": ["foo", "bar"], "api_key": vault.get("API_KEY")}
