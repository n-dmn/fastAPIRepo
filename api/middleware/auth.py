from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Very basic authentication middleware."""

    async def dispatch(self, request, call_next):  # type: ignore[override]
        token = request.headers.get("Authorization")
        if token != "Bearer secret-token":
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
        return await call_next(request)
