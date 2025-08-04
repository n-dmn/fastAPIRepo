from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies import get_keyvault, set_keyvault
from api.middleware.auth import AuthenticationMiddleware
from api.routes import example
from core.keyvault import KeyVault
from core.database import init_db

app = FastAPI()

# Middleware
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(example.router)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize KeyVault once at startup."""
    init_db()
    set_keyvault(KeyVault())


@app.get("/ping")
async def ping(kv: KeyVault = Depends(get_keyvault)):
    return {"message": "pong", "api_key": kv.get("API_KEY")}
