"""Mock server with streaming endpoints for testing pytest-openapi streaming support."""

import json
import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="Streaming API Test Server",
    description="Test server with SSE and NDJSON streaming endpoints",
    version="1.0.0",
    docs_url=None,  # Disable automatic docs
    redoc_url=None,  # Disable automatic redoc
    openapi_url=None,  # Disable automatic openapi.json
)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/reset")
async def reset():
    """Reset server state (for testing)."""
    return {"status": "reset"}


async def generate_sse_stream():
    """Generate Server-Sent Events stream."""
    # Send a few chunks
    for i in range(3):
        chunk_data = {
            "id": i,
            "message": f"Chunk {i}",
            "timestamp": int(time.time()),
        }
        yield f"data: {json.dumps(chunk_data)}\n\n"

    # Send final message
    yield "data: [DONE]\n\n"


async def generate_ndjson_stream():
    """Generate newline-delimited JSON stream."""
    # Send a few chunks
    for i in range(3):
        chunk_data = {
            "id": i,
            "message": f"Chunk {i}",
            "timestamp": int(time.time()),
        }
        yield json.dumps(chunk_data) + "\n"

    # Send final message
    yield json.dumps({"done": True}) + "\n"


@app.post("/stream/sse")
async def stream_sse(request: dict):
    """Stream response using Server-Sent Events format."""
    return StreamingResponse(
        generate_sse_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.post("/stream/ndjson")
async def stream_ndjson(request: dict):
    """Stream response using newline-delimited JSON format."""
    return StreamingResponse(
        generate_ndjson_stream(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
        },
    )


@app.post("/chat")
async def chat(request: dict):
    """Regular JSON endpoint for comparison."""
    message = request.get("message", "")
    stream = request.get("stream", False)

    if stream:
        # Return streaming response
        return StreamingResponse(
            generate_sse_stream(),
            media_type="text/event-stream",
        )
    else:
        # Return regular JSON
        return {
            "response": f"Echo: {message}",
            "timestamp": int(time.time()),
        }


@app.get("/openapi.json")
async def get_openapi():
    """Return OpenAPI spec with streaming endpoints documented."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Streaming API Test Server",
            "version": "1.0.0",
            "description": "Test server with SSE and NDJSON streaming endpoints",
        },
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health check",
                    "description": "Check if the server is running",
                    "responses": {
                        "200": {
                            "description": "Server is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Health status",
                                            }
                                        },
                                        "required": ["status"],
                                    },
                                    "example": {"status": "ok"},
                                }
                            },
                        }
                    },
                }
            },
            "/stream/sse": {
                "post": {
                    "summary": "Stream using Server-Sent Events",
                    "description": "Returns a streaming response in SSE format",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "description": "Message to process",
                                        }
                                    },
                                    "required": ["message"],
                                },
                                "example": {"message": "test"},
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Streaming response",
                            "content": {
                                "text/event-stream": {
                                    "schema": {
                                        "type": "string",
                                        "description": "Server-Sent Events stream",
                                    },
                                    "example": 'data: {"message": "chunk"}\n\n',
                                }
                            },
                        }
                    },
                }
            },
            "/stream/ndjson": {
                "post": {
                    "summary": "Stream using newline-delimited JSON",
                    "description": "Returns a streaming response in NDJSON format",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "description": "Message to process",
                                        }
                                    },
                                    "required": ["message"],
                                },
                                "example": {"message": "test"},
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Streaming response",
                            "content": {
                                "application/x-ndjson": {
                                    "schema": {
                                        "type": "string",
                                        "description": "Newline-delimited JSON stream",
                                    },
                                    "example": '{"message": "chunk"}\n',
                                }
                            },
                        }
                    },
                }
            },
            "/chat": {
                "post": {
                    "summary": "Chat endpoint with optional streaming",
                    "description": "Returns JSON or stream based on stream parameter",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "description": "Message to send",
                                        },
                                        "stream": {
                                            "type": "boolean",
                                            "description": "Whether to stream response",
                                            "default": False,
                                        },
                                    },
                                    "required": ["message"],
                                },
                                "example": {
                                    "message": "hello",
                                    "stream": False,
                                },
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Chat response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "response": {
                                                "type": "string",
                                                "description": "Response message",
                                            },
                                            "timestamp": {
                                                "type": "integer",
                                                "description": "Unix timestamp",
                                            },
                                        },
                                        "required": ["response", "timestamp"],
                                    },
                                    "example": {
                                        "response": "Echo: hello",
                                        "timestamp": 1703347200,
                                    },
                                }
                            },
                        }
                    },
                }
            },
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
