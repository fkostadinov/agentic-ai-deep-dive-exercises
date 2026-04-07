# Exercise Tic-Tac-Toe - Simulate a Simple A2A Client/Server System

## Goal of this exercise

In this exercise, you will build and explore a very small **Agent-to-Agent (A2A)** style system using a Tic-Tac-Toe game.

Instead of focusing on language-model reasoning, this exercise focuses on **architecture**:

* a client sends requests
* a server receives and executes them
* the server returns structured events
* state lives on the server across multiple requests

The game itself is intentionally simple so that you can concentrate on the interaction pattern.

---

## What you will learn

By the end of this exercise, you will understand:

* how to model a simple **client/server agent interaction**
* how a request can produce a stream or list of **events**
* why **request context** is short-lived while **agent state** is persistent
* how to separate:

  * client logic
  * server logic
  * shared protocol types
* how to structure a small Python project into clear packages

---

## What you will build

You will build a Tic-Tac-Toe system with:

* a **client CLI** that accepts user commands
* a **server process** that owns the game state
* a shared event model inspired by A2A concepts

Supported commands:

* `new` - start a new game
* `show` - print the current board
* `move <row> <col>` - place the next mark
* `exit` - quit the client

The board is rendered with row and column numbers from `0` to `2`.

---

## Architecture overview

The system now follows this flow:

```text
User
  ->
Client CLI (client-app.py)
  ->
A2AClient
  ->
TCP transport (localhost)
  ->
A2A TCP Server (server-app.py)
  ->
AgentExecutor
  ->
TicTacToeAgent
  ->
GameState
```

Key idea:

* The **client** creates a new request for every user command.
* The **server** keeps the long-lived game state alive between commands.

---

## Project structure

```text
exercise-tic-tac-toe/
|-- client-app.py
|-- server-app.py
|-- requirements.txt
|-- .env.example
|-- client/
|   |-- __init__.py
|   `-- client.py
|-- server/
|   |-- __init__.py
|   |-- server.py
|   |-- executor.py
|   |-- game_agent.py
|   `-- game_state.py
`-- shared/
    |-- __init__.py
    |-- a2a_types.py
    `-- transport.py
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

Note:

* The current Tic-Tac-Toe implementation only uses the Python standard library.
* The `requirements.txt` file is kept for consistency with the other exercises.

---

## Running the system

You need **two terminals**.

### Terminal 1 - Start the server

```bash
python server-app.py
```

You should see:

```text
A2A Tic-Tac-Toe server listening on 127.0.0.1:8765
```

---

### Terminal 2 - Start the client

```bash
python client-app.py
```

You can then enter commands such as:

```text
new
move 0 0
move 1 1
show
```

---

## Example interaction

```text
> new
[TASK] submitted
[STATUS] working - Processing request...
[ARTIFACT]
Board:
  0 1 2
0 . . .
1 . . .
2 . . .
Next player: X
[STATUS] completed
```

```text
> move 1 2
[TASK] submitted
[STATUS] working - Processing request...
[ARTIFACT]
Move accepted.

Board:
  0 1 2
0 . . .
1 . . X
2 . . .
Next player: O
[STATUS] completed
```

---

## How it works

Each user command follows this sequence:

1. The client reads terminal input
2. The client creates a new `RequestContext`
3. The client sends the request to the server over localhost TCP
4. The server executes the request through `AgentExecutor`
5. The Tic-Tac-Toe agent updates or reads the game state
6. The server returns structured events
7. The client prints those events to the console

---

## Important concept: Request state vs. game state

This exercise is useful because it makes an important distinction explicit:

* **Request state** is short-lived

  * request ID
  * context ID
  * event queue

* **Game state** is persistent

  * board contents
  * next player
  * winner / draw status

A new request is created for every command, but the game only resets when the user sends `new`.

---

## Important concept: Why the client does not hold a server object

In an earlier in-process version, the client directly referenced the server object.

In the current version, the client talks to the server through a **transport boundary**:

* the client serializes a request
* the server deserializes it
* the server serializes events
* the client deserializes them

This is closer to how real distributed systems work.

---

## Your tasks

### Task 1 - Run the server and client

Verify that both processes start and can communicate.

---

### Task 2 - Play a full game

Try a complete Tic-Tac-Toe session and observe:

* state persists across moves
* the board prints row/column numbers
* the server owns the game state

---

### Task 3 - Inspect the protocol types

Look at:

* `shared/a2a_types.py`
* `shared/transport.py`

Understand how requests and events are represented and serialized.

---

### Task 4 - Trace the architecture

Follow one command end-to-end:

```text
move 0 0
```

Trace the flow through:

* `client-app.py`
* `client/client.py`
* `server/server.py`
* `server/executor.py`
* `server/game_agent.py`
* `server/game_state.py`

---

### Task 5 - Extend the protocol or game

Try one of the following:

* add a `help` command
* add a `reset` alias for `new`
* add server-side logging for requests
* add a new event type
* make the server reject malformed requests explicitly

---

## Optional challenges

If you finish early, try:

* persist game state to disk
* support multiple concurrent games with session IDs
* replace the raw TCP transport with HTTP
* add automated tests for client/server communication
* add a second agent that can play automatically

---

## Key takeaway

This exercise shows that an A2A-style system is not primarily about model calls.

It is about **clear boundaries**:

* who sends requests
* who owns state
* how messages are transported
* how results are represented

By keeping the game simple, you can focus on the architecture that more advanced multi-agent systems are built on.
