from urllib.parse import urlparse

import httpx
from mcp.server.mcpserver import Image, MCPServer

mcp = MCPServer("image-fetch")

MAX_BYTES = 20 * 1024 * 1024
ALLOWED_SCHEMES = {"http", "https"}

MIME_TO_FORMAT = {
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/jpg": "jpeg",
    "image/webp": "webp",
    "image/gif": "gif",
}


@mcp.tool()
async def fetch_image(url: str) -> Image:
    """Fetch an HTTP(S) image URL and return it as MCP ImageContent."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("Only http:// and https:// URLs are allowed")

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=20.0,
        headers={"User-Agent": "Lambda6-image-fetch/1.0"},
    ) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if content_type not in MIME_TO_FORMAT:
                raise ValueError(f"Unsupported image Content-Type: {content_type or 'missing'}")

            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > MAX_BYTES:
                raise ValueError(f"Image is larger than {MAX_BYTES // (1024 * 1024)} MiB")

            chunks = []
            size = 0
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > MAX_BYTES:
                    raise ValueError(f"Image is larger than {MAX_BYTES // (1024 * 1024)} MiB")
                chunks.append(chunk)

    return Image(data=b"".join(chunks), format=MIME_TO_FORMAT[content_type])


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8765,
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
    )

