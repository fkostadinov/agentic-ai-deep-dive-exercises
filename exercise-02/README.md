# Exercise 02 – Build a Stateful CLI Agent (with SDK)

## Goal of this exercise

In this exercise, you will extend your agent from Exercise 01 into a **stateful conversational agent**.

Instead of responding once, your agent will now:

* run in a loop
* remember previous interactions
* decide whether to **answer immediately** or **guide the user step-by-step**

You will also replace raw HTTP calls with the **OpenAI SDK**, which simplifies interaction with the model.

---

## What you will learn

By the end of this exercise, you will understand:

* How to build a **stateful agent loop**
* How to manage **conversation history (memory)**
* When an agent should **act immediately vs. plan**
* How an SDK simplifies API usage compared to raw HTTP
* How structured outputs guide agent behavior

---

## What you will build

You will build a command-line agent that:

* accepts user input continuously
* keeps conversation context across turns
* decides between:

  * answering directly (e.g. “tell me a joke”)
  * asking follow-up questions or refining a plan
* supports basic commands like `reset`, `history`, and `exit`

---

## Example interaction

```text
You: Tell me a joke

Agent:
Why do programmers prefer dark mode? Because light attracts bugs.
```

```text
You: Help me prepare a workshop on AI agents

Agent:
A good starting point is to define the target audience and learning objectives.

Plan:
1. Define the audience
2. Choose key topics
3. Draft the agenda

Next action:
Tell me who the workshop is for and how long it should be.
```

---

## Key concept: Answer vs. Follow-up

In Exercise 01, your agent always planned first.

In this exercise, the agent must decide:

* **Answer mode** → do the task immediately
* **Follow-up mode** → guide the user through multiple steps

This is a key step toward building realistic agents.

---

## Project structure

```text
exercise-02-stateful-agent/
├── agent.py
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
```

---

## Run the agent

```bash
python agent.py
```

---

## Commands

The agent supports:

* `exit` / `quit` → stop the program
* `reset` → clear memory
* `history` → print conversation history

---

## How it works (conceptually)

The agent loop looks like this:

1. Read user input
2. Append it to message history
3. Send full history to the model
4. Receive structured JSON response
5. Print result
6. Append response to history
7. Repeat

The “memory” is simply the list of messages.

---

## Your tasks

### Task 1 – Run the agent

Verify that the agent works across multiple turns.

---

### Task 2 – Test both modes

Try:

* A simple request:

  ```text
  Tell me a joke
  ```
* A complex task:

  ```text
  Help me design a training on AI agents
  ```

Observe the difference in behavior.

---

### Task 3 – Inspect memory

Use:

```text
history
```

Look at how messages are stored and passed to the model.

---

### Task 4 – Refine a task over time

Example:

```text
I want to prepare a workshop on AI agents
Make it more technical
Add a section on security
```

Observe how the plan evolves.

---

### Task 5 – Reset state

Use:

```text
reset
```

Confirm that the agent forgets previous context.

---

## Important concept: Memory

The agent does not “remember” magically.

Its memory is explicitly managed as:

* a list of messages
* sent to the model on every request

This is the foundation for more advanced memory systems later.

---

## Important concept: SDK vs. raw HTTP

In Exercise 01, you:

* manually built HTTP requests

In Exercise 02, you:

* use an SDK (`openai`)

The underlying logic is the same — the SDK simply abstracts:

* request construction
* authentication
* response handling

---

## Optional challenges

If you finish early, try:

* Limit history to the last N turns
* Add a `help` command
* Save conversations to a file
* Print both raw and parsed responses
* Add timestamps to messages

---

## Key takeaway

A stateful agent is still built from simple components:

* input
* memory (message history)
* model call
* structured output

The main difference is that the agent now:

* operates over time
* adapts based on context
* decides when to act vs. when to guide
