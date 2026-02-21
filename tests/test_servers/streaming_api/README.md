# Streaming API Test Server

Mock server for testing pytest-openapi's handling of streaming responses.

## Endpoints

### POST /stream/sse
Returns a Server-Sent Events (SSE) stream using `Content-Type: text/event-stream`.

**Request:**
```json
{
  "message": "test"
}
```

**Response:** SSE stream with multiple chunks followed by `[DONE]` marker.

### POST /stream/ndjson
Returns a newline-delimited JSON stream using `Content-Type: application/x-ndjson`.

**Request:**
```json
{
  "message": "test"
}
```

**Response:** NDJSON stream with multiple chunks followed by a `done: true` marker.

### POST /chat
Dual-mode endpoint that returns either JSON or streaming response based on the `stream` parameter.

**Request:**
```json
{
  "message": "hello",
  "stream": false
}
```

**Response (stream=false):** Regular JSON response
```json
{
  "response": "Echo: hello",
  "timestamp": 1703347200
}
```

**Response (stream=true):** SSE stream (same as `/stream/sse`)

## Purpose

This server tests that pytest-openapi correctly:
1. Detects streaming responses by checking `Content-Type` headers
2. Handles SSE format (`text/event-stream`)
3. Handles NDJSON format (`application/x-ndjson`)
4. Doesn't try to parse streaming responses as JSON
5. Validates streaming endpoints return correct status codes
6. Works with schema-generated tests that may include `stream: true`
