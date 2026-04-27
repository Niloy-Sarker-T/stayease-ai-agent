# StayEase API Contract

## 1. Send a Guest Message

### POST /api/chat/{conversation_id}/message

Sends a guest message to the AI agent and returns the agent's response.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| conversation_id | string | Unique conversation session ID |

**Request Body:**

```json
{
  "message": "string"
}
```

**Response (200 OK):**

```json
{
  "conversation_id": "string",
  "role": "assistant",
  "content": "string",
  "timestamp": "string (ISO 8601)"
}
```

**Example Request:**

    POST /api/chat/conv-001/message
    Content-Type: application/json

    {
      "message": "I need a room in Cox's Bazar for 2 nights for 2 guests"
    }

**Example Response:**

    {
      "conversation_id": "conv-001",
      "role": "assistant",
      "content": "I found 2 available properties in Cox's Bazar for 2 nights for 2 guests:\n\n1. Sea Pearl Hotel — BDT 4,500/night, Rating 4.5\n2. Ocean View Resort — BDT 6,200/night, Rating 4.8\n\nWould you like to see details for any of these?",
      "timestamp": "2025-01-15T10:30:00Z"
    }

**Error Responses:**

| Status | Description | Body |
|--------|-------------|------|
| 400 Bad Request | Empty or missing message field | {"error": "Message field is required"} |
| 500 Internal Server Error | Agent or LLM failure | {"error": "Failed to process message. Please try again."} |

---

## 2. Get Conversation History

### GET /api/chat/{conversation_id}/history

Returns all messages in a conversation, ordered chronologically.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| conversation_id | string | Unique conversation session ID |

**Response (200 OK):**

```json
{
  "conversation_id": "string",
  "messages": [
    {
      "role": "user or assistant",
      "content": "string",
      "timestamp": "string (ISO 8601)"
    }
  ]
}
```

**Example Request:**

    GET /api/chat/conv-001/history

**Example Response:**

    {
      "conversation_id": "conv-001",
      "messages": [
        {
          "role": "user",
          "content": "I need a room in Cox's Bazar for 2 nights for 2 guests",
          "timestamp": "2025-01-15T10:29:55Z"
        },
        {
          "role": "assistant",
          "content": "I found 2 available properties in Cox's Bazar...",
          "timestamp": "2025-01-15T10:30:00Z"
        },
        {
          "role": "user",
          "content": "Tell me more about Sea Pearl Hotel",
          "timestamp": "2025-01-15T10:31:10Z"
        },
        {
          "role": "assistant",
          "content": "Sea Pearl Hotel — Cox's Bazar. Beachfront hotel. BDT 4,500/night. Rating 4.5. Amenities: WiFi, AC, Breakfast, Pool, Parking. Would you like to book?",
          "timestamp": "2025-01-15T10:31:15Z"
        }
      ]
    }

**Error Responses:**

| Status | Description | Body |
|--------|-------------|------|
| 404 Not Found | Conversation ID does not exist | {"error": "Conversation not found"} |
| 500 Internal Server Error | Database query failure | {"error": "Failed to retrieve conversation history"} |