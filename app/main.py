"""FastAPI client for interacting with the Petstore MCP server via Azure OpenAI."""
from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from openai_agents.mcp import MCPClient


AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "ws://localhost:8080")


class ChatRequest(BaseModel):
    message: str


app = FastAPI(title="Petstore Client")


@app.on_event("startup")
async def startup_event() -> None:
    """Validate configuration on startup."""
    missing = [
        name
        for name in (
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION",
        )
        if not globals()[name]
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


def _get_client() -> AzureOpenAI:
    """Create an Azure OpenAI client."""
    return AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
    )


@app.post("/chat")
async def chat(req: ChatRequest) -> dict[str, Any]:
    """Send a message to the Azure OpenAI model with access to the MCP server."""
    client = _get_client()
    mcp = MCPClient.from_url(MCP_SERVER_URL)
    try:
        response = await client.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            input=[{"role": "user", "content": req.message}],
            tools=[mcp],
        )
    except Exception as exc:  # pragma: no cover - network errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"response": response.output_text}
