# FastAPI Petstore MCP Example

This repository contains a minimal example demonstrating how to expose the
[Swagger Petstore](https://petstore.swagger.io/) API to an OpenAI agent via the
Model Context Protocol (MCP). A FastAPI application acts as a client that sends
requests to Azure OpenAI and grants it access to the MCP server.

## Structure

- `app/mcp_server.py` – wraps the Petstore OpenAPI spec in an MCP server.
- `app/main.py` – FastAPI application that calls Azure OpenAI with the MCP tool.
- `requirements.txt` – Python dependencies.

## Environment variables

Configure the following variables before running the server and client:

```bash
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="..."
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"
```

Optionally override `MCP_SERVER_URL` if the MCP server runs on a different host.

## Usage

```bash
# Start the MCP server
python app/mcp_server.py

# Run the FastAPI app
uvicorn app.main:app --reload
```

## Testing

```bash
pytest
```
