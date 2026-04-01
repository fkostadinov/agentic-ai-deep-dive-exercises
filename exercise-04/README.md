# Exercise 04 – Build an MCP-Based Agent (HTTP)

## Goal of this exercise

In this exercise, you will refactor your tool-using agent to use the **Model Context Protocol (MCP)** over HTTP.

Instead of calling Python functions directly, your agent will now:

* connect to an MCP server over HTTP
* discover available tools dynamically
* call tools via a standardized interface

The functionality stays the same — but the architecture becomes **modular and extensible**.

---

## What you will learn

By the end of this exercise, you will understand:

* What MCP (Model Context Protocol) is
* How agents can **discover tools dynamically**
* How to connect to an MCP server over HTTP
* How to call tools via MCP instead of direct function calls
* Why decoupling agents and tools is important

---

## What you will build

You will build a CLI agent that:

* connects to an MCP server
* lists available tools
* calls tools via MCP
* produces final responses based on tool results

---

## Key concept: From local tools → MCP

In Exercise 03:

```text
Agent → Python functions
```

In Exercise 04:

```text
Agent → MCP client → MCP server → tools
```

This means:

* the agent no longer knows how tools are implemented
* tools can run in a separate process or machine
* tools can be reused across multiple agents

---

## Architecture overview

```text
User
  ↓
Agent (LLM)
  ↓
MCP Client (HTTP)
  ↓
MCP Server (/mcp)
  ↓
Tools (Python functions)
```

---

## Project structure

```text
exercise-04-mcp-agent/
├── agent.py
├── mcp_server.py
├── tools.py
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Create a virtual environment

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Example:

```txt
openai
python-dotenv
mcp
```

---

### 3. Configure environment variables

Copy:

```bash
cp .env.example .env
```

Fill in:

```env
FOUNDRY_ENDPOINT=...
FOUNDRY_API_KEY=...
FOUNDRY_MODEL=...
MCP_SERVER_URL=http://127.0.0.1:8000/mcp
```

---

## Running the system

You need **two terminals**.

### Terminal 1 – Start MCP server

```bash
python mcp_server.py
```

This starts the MCP server at:

```text
http://127.0.0.1:8000/mcp
```

---

### Terminal 2 – Run agent

```bash
python agent.py
```

---

## Example interactions

```text
You: What time is it?

Agent:
The current time is 2026-04-01 10:15:23.
```

```text
You: Calculate 25 * 4 + 3

Agent:
The result is 103.
```

```text
You: Save a note saying buy coffee

Agent:
Your note has been saved.
```

---

## Commands

* `exit` / `quit` → stop the program
* `reset` → clear conversation memory
* `history` → show message history
* `tools` → list available MCP tools

---

## How it works (step-by-step)

Each request follows this flow:

1. User input
2. Model decides:

   * `"answer"` → respond directly
   * `"tool_call"` → call a tool
3. If tool is needed:

   * MCP client sends request to server
   * server executes Python function
   * result is returned
4. Model generates final response

---

## Key concept: Tool discovery

Unlike Exercise 03, tools are not hardcoded.

The agent asks the MCP server:

```python
await session.list_tools()
```

This returns available tools dynamically.

---

## Key concept: Decoupling

Exercise 03:

* agent tightly coupled to tools

Exercise 04:

* agent and tools are separated via MCP

Benefits:

* reusable tools
* independent deployment
* easier scaling
* cleaner architecture

---

## Your tasks

### Task 1 – Run the MCP server

Start `mcp_server.py` and verify it runs without errors.

---

### Task 2 – Connect the agent

Run `agent.py` and confirm it prints available tools.

---

### Task 3 – Test all tools

Try:

```text
What time is it?
Calculate 144 / 12 + 7
Save a note saying test MCP
```

---

### Task 4 – Inspect tool discovery

Use:

```text
tools
```

Observe:

* tool names
* dynamic availability

---

### Task 5 – Trace the flow

Understand:

```text
User → Agent → MCP → Tool → MCP → Agent → User
```

---

## Important concept: Transport

In this exercise, MCP uses **HTTP**:

```text
http://127.0.0.1:8000/mcp
```

This is:

* more stable than stdio on Windows
* closer to real-world deployments
* compatible with HTTPS (encryption)

---

## Optional challenges

If you finish early:

* Add a new tool (e.g. `read_notes`)
* Change tool descriptions to improve selection
* Log all tool calls
* Move MCP server to another machine
* Add HTTPS (advanced)

---

## Key takeaway

MCP introduces a **standard interface between agents and tools**.

This allows:

* separation of concerns
* dynamic tool discovery
* scalable architectures
