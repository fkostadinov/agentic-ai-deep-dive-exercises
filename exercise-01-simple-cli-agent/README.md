# Exercise 01 – Build a Simple CLI Agent (from Scratch)

## Goal of this exercise

In this exercise, you will build your **first software agent from scratch** using Python and a raw HTTP call to a language model hosted on Microsoft Foundry.

You will **not use any frameworks or SDK abstractions**. The purpose is to clearly understand what an agent actually is at its core.

---

## What you will learn

By the end of this exercise, you will understand:

* What a **software agent loop** looks like
* How to call a **language model via HTTP**
* How to structure **system + user prompts**
* How to enforce **structured (JSON) outputs**
* How to parse and display model responses

---

## What you will build

You will build a simple **command-line agent** that:

1. Accepts a user goal (e.g. “Plan a 2-hour study session”)
2. Sends this goal to a model via HTTP
3. Receives a structured response
4. Prints:

   * a short restatement of the goal
   * a step-by-step plan
   * the next best action

Example:

```text
Goal: Prepare a 10-minute presentation on AI agents

Plan:
1. Define what an AI agent is
2. Explain the core loop (input → reasoning → action)
3. Give a simple example
4. Create 3–4 slides
5. Rehearse timing

Next action:
Write a one-sentence definition of an AI agent.
```

---

## Why “from scratch”?

In this exercise, we intentionally avoid frameworks.

This helps you clearly see the core components of an agent:

* Input (goal)
* Prompt (instructions)
* Model call (reasoning)
* Output (actionable result)

Later exercises will introduce abstractions — but only after you understand the fundamentals.

---

## Project structure

```text
exercise-01-simple-agent/
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

Copy the example file:

```bash
cp .env.example .env
```

Then fill in your values:

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

Then enter a goal:

```text
Goal: Plan a weekend trip to Zurich
```

---

## How it works (high level)

Your agent performs the following steps:

1. Read user input from the terminal
2. Build a prompt (system + user message)
3. Send an HTTP POST request to the model
4. Receive a response
5. Parse JSON
6. Print structured output

This is the **core agent loop**.

---

## Important design choice: JSON output

The model is instructed to return **strict JSON**.

This makes the agent:

* easier to parse
* more predictable
* easier to extend later

---

## Your tasks

### Task 1 – Run the agent

Make sure everything works end-to-end.

---

### Task 2 – Inspect the request

Look at:

* the payload sent to the model
* the structure of messages

---

### Task 3 – Inspect the response

Print the full raw response:

```python
print(json.dumps(response.json(), indent=2))
```

Understand:

* where the actual content is
* how it is structured

---

### Task 4 – Modify the behavior

Try one of the following:

* Change the system prompt tone (e.g. “be more concise”)
* Force exactly 3 steps instead of 3–5
* Add a `"risks"` field to the output

---

## Optional challenges

If you finish early:

* Add input validation (empty input, bad JSON)
* Pretty-print the output
* Save the result to a file (`output.json`)

---

## Key takeaway

An “agent” is not magic.

At its core, it is simply:

> A loop that sends structured input to a model and turns the output into actionable steps.

Everything else (tools, memory, multi-agent systems) builds on top of this.
