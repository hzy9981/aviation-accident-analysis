FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for document parsing
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

# Default command to run the MCP server (SSE mode is better for long-running containers)
# Note: FastMCP supports SSE via mcp.run(transport='sse') or similar if configured
# For now we'll keep it flexible, but usually containers run as SSE servers.
CMD ["uv", "run", "mcp_server.py"]
