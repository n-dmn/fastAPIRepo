"""Placeholder MCP server using the same routers as the FastAPI app."""

from fastapi import FastAPI

from ..routers import example


def create_mcp_server() -> FastAPI:
    """Create an MCP-compatible server with shared routers."""
    server = FastAPI()
    server.include_router(example.router)
    return server
