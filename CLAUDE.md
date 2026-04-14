# WiFi Query MCP Server - Claude Development Guide

## Project Overview

This is a simple MCP (Model Context Protocol) server that provides a `get_wifi_password` tool for Claude to retrieve a pre-configured WiFi password.

## Development Commands

- **Check syntax**: `python -m py_compile server.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Run server**: `python server.py`
- **Test health endpoint**: `curl http://localhost:8000/health`
- **List tools**: `curl -X POST http://localhost:8000/mcp`

## Code Style

- Follow PEP 8
- Keep functions small and focused
- Use type hints
- Document public functions with docstrings

## MCP Configuration

The MCP server endpoint is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "wifi-query": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Environment Variables for Development

When testing locally, you can set environment variables:
```bash
export WIFI_PASSWORD="test_password"
export PORT=8001
```

## Security Notes

- By default binds to `127.0.0.1` for local access only
- If exposed to public network, add appropriate authentication
- Never commit actual WiFi passwords to git
