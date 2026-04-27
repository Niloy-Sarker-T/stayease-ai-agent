# 🏨 StayEase AI Agent

## 1.1 🌐 System Overview

**StayEase** is an AI-powered booking agent for a short-term accommodation rental platform in Bangladesh. Guests interact with the agent through a chat interface to search for available properties, view listing details, and make bookings.

The system architecture utilizes:
- **FastAPI** backend to handle HTTP requests.
- **LangGraph** agent to orchestrate conversation flow and tool usage.
- **PostgreSQL** for persistent storage.
- **Groq LLM (`Llama 3 70B`)** for natural language understanding and response generation.

> **Note:** If the agent cannot handle a request, it automatically **escalates** the conversation to a human operator.

### Architecture Diagram

```mermaid
graph TD
    A[Guest / Chat UI] -->|HTTP Request| B[FastAPI Backend]
    B -->|Invoke Agent| C[LangGraph Agent]
    C -->|LLM Calls| D[Groq LLM - Llama 3 70B]
    C -->|Tool Calls| E[Tools Layer]
    E -->|SQL Queries| F[PostgreSQL Database]
    B -->|Read/Write Conversations| F
    C -->|Escalate| G[Human Operator]
```

---

## 1.2 💬 Conversation Flow

**Example Scenario:**
Guest says: *"I need a room in Cox's Bazar for 2 nights for 2 guests."*

| Step | Component | What Happens |
|------|-----------|-------------|
| 1 | **FastAPI** | Receives POST request at `/api/chat/{conversation_id}/message`. Saves message to the `conversations` table. |
| 2 | **parse_input node** | LLM extracts: `location="Cox's Bazar"`, `check_in=2025-01-15`, `check_out=2025-01-17`, `guests=2`. |
| 3 | **route node** | Intent is `search`, so agent routes to `use_tool` node with `search_available_properties`. |
| 4 | **use_tool node** | Calls `search_available_properties(...)`. Queries PostgreSQL. Returns matching listings. |
| 5 | **respond node** | LLM formats results into a friendly message with property names, prices in BDT, and ratings. |
| 6 | **FastAPI** | Saves agent response to `conversations` table and returns it in the HTTP response. |

---

## 1.3 🧠 LangGraph State Design

    class AgentState(TypedDict):
        messages: list[BaseMessage]        # Full conversation history for LLM context
        intent: str                        # Parsed intent: search | details | book | escalate
        tool_name: str                     # Which tool to invoke next
        tool_input: dict                   # Parameters to pass to the selected tool
        tool_output: dict                  # Result returned from the tool
        conversation_id: str               # Links this agent run to a stored conversation

| Field | Why it's needed |
|-------|----------------|
| `messages` | LLM needs the full conversation history to understand context. |
| `intent` | Determines which path the agent takes through the graph. |
| `tool_name` | Tells the `use_tool` node which specific tool to call. |
| `tool_input` | Carries extracted parameters from the user message to the tool. |
| `tool_output` | Stores tool results so the `respond` node can format them. |
| `conversation_id` | Associates the agent session with the persisted conversation in the database. |

---

## 1.4 🔄 Node Design

| Node | What it does | State updates | Next node |
|------|-------------|---------------|-----------|
| **parse_input** | Uses the LLM to extract intent and parameters from the latest user message. | `intent`, `tool_name`, `tool_input` | route |
| **route** | Conditional node that directs flow based on the intent. | *(no update — routing only)* | use_tool or escalate |
| **use_tool** | Calls the selected tool with the extracted parameters. | `tool_output` | respond |
| **respond** | Uses the LLM to format tool output into a natural language reply. | `messages` (appends AI response) | END |
| **escalate** | Returns a handoff message telling the guest a human will help. | `messages` (appends escalation message) | END |

---

## 1.5 🛠️ Tool Definitions

### 🔍 search_available_properties

- **When used:** Guest wants to find available properties (intent = `search`).
- **Input:** `location: str`, `check_in: str (YYYY-MM-DD)`, `check_out: str (YYYY-MM-DD)`, `guests: int`
- **Output:** `list[{ listing_id, name, location, price_per_night, rating, max_guests }]`

### ℹ️ get_listing_details

- **When used:** Guest asks about a specific property (intent = `details`).
- **Input:** `listing_id: int`
- **Output:** `{ listing_id, name, location, description, price_per_night, rating, max_guests, amenities }`

### 📅 create_booking

- **When used:** Guest confirms they want to book a property (intent = `book`).
- **Input:** `listing_id: int`, `guest_name: str`, `check_in: str (YYYY-MM-DD)`, `check_out: str (YYYY-MM-DD)`, `guests: int`
- **Output:** `{ booking_id, listing_name, total_price, status }`

---

## 1.6 🗄️ Database Schema

### 🏠 listings

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique listing ID |
| name | VARCHAR(255) | Property name |
| location | VARCHAR(255) | City/area in Bangladesh |
| description | TEXT | Property description |
| price_per_night | DECIMAL(10,2) | Price in BDT |
| max_guests | INTEGER | Maximum occupancy |
| rating | DECIMAL(2,1) | Average rating 0.0–5.0 |
| amenities | TEXT[] | List of amenities |
| is_available | BOOLEAN DEFAULT TRUE | Whether listing is active |
| created_at | TIMESTAMP DEFAULT NOW() | Record creation time |

### 🎟️ bookings

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique booking ID |
| listing_id | INTEGER REFERENCES listings(id) | Booked property |
| guest_name | VARCHAR(255) | Name of the guest |
| check_in | DATE | Check-in date |
| check_out | DATE | Check-out date |
| guests | INTEGER | Number of guests |
| total_price | DECIMAL(10,2) | Total cost in BDT |
| status | VARCHAR(50) DEFAULT confirmed | Booking status |
| created_at | TIMESTAMP DEFAULT NOW() | Record creation time |

### 💬 conversations

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique message ID |
| conversation_id | VARCHAR(100) | Groups messages in one chat session |
| role | VARCHAR(20) | user or assistant |
| content | TEXT | Message text |
| created_at | TIMESTAMP DEFAULT NOW() | Message timestamp |