import os
from typing import Any


class KeyVault:
    """Simple KeyVault abstraction loaded once at startup."""

    def __init__(self) -> None:
        self._secrets: dict[str, Any] = {
            "API_KEY": os.getenv("API_KEY"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "DATABASE_SCHEMA": os.getenv("DATABASE_SCHEMA", "app_schema"),
        }

    def get(self, key: str) -> Any:
        return self._secrets.get(key)
