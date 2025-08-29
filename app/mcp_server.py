"""MCP server exposing the Petstore OpenAPI specification."""
from __future__ import annotations

from openai_agents import openapi

PETSTORE_SPEC = "https://petstore.swagger.io/v2/swagger.json"


def create_server() -> openapi.OpenAPIServer:
    """Create an MCP server backed by the Petstore OpenAPI spec."""
    return openapi.OpenAPIServer.from_url(PETSTORE_SPEC)


def main() -> None:
    """Entrypoint for running the Petstore MCP server."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
