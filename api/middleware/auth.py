from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Optional

import jwt
from jwt import PyJWKClient

from dependencies import get_keyvault


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Validate Azure AD access tokens for incoming requests."""

    def __init__(self, app):
        super().__init__(app)
        self._jwk_client: Optional[PyJWKClient] = None
        self._issuer: Optional[str] = None
        self._audience: Optional[str] = None

    def _ensure_client(self) -> None:
        if self._jwk_client is None:
            kv = get_keyvault()
            tenant_id = kv.get("AZURE_TENANT_ID")
            audience = kv.get("AZURE_CLIENT_ID")
            if not tenant_id or not audience:
                raise RuntimeError("Azure AD configuration missing")
            self._issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
            jwks_url = f"{self._issuer}/discovery/v2.0/keys"
            self._jwk_client = PyJWKClient(jwks_url)
            self._audience = audience

    async def dispatch(self, request, call_next):  # type: ignore[override]
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        token = auth_header.split(" ", 1)[1]

        try:
            self._ensure_client()
            assert self._jwk_client and self._issuer and self._audience
            signing_key = self._jwk_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self._issuer,
            )
            request.state.user = payload.get("sub")
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        return await call_next(request)
