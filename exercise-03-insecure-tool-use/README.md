# Exercise 03 – Build a Tool-Using CLI Agent

## Goal of this exercise

In this exercise, you will extend your agent so that it can **use tools (i.e. Python functions)** to perform real actions.

Until now, your agent could:

* respond with text (Exercise 01)
* maintain memory and context (Exercise 02)

Now it will:

* **decide when to call a tool**
* **execute Python code**
* **use the result to produce a final answer**

---

## What you will learn

By the end of this exercise, you will understand:

* What **tool use** means in agent systems
* How to represent tools as **plain Python functions**
* How an agent decides between:

  * answering directly
  * calling a tool
* The **two-step interaction pattern**:

  1. decide what to do
  2. produce final response after action
* How tools make agents **more reliable and useful**

---

## What you will build

You will build a CLI agent that can:

* answer simple questions directly
* call tools when needed
* execute Python functions
* return a final user-facing response

---

## Example interactions

```text
You: What time is it?

Agent:
The current time is 2026-03-31 14:32:10.
```

```text
You: Calculate 17 * 23 + 4

Agent:
The result is 395.
```

```text
You: Save a note saying buy milk and eggs

Agent:
Your note has been saved.
```

---

## Key concept: Tools

A tool is simply:

> A Python function that the agent can decide to call

Example:

```python
def get_current_time():
    ...
```

The agent does not execute code directly.
Instead, it:

1. decides which tool to use
2. provides inputs
3. your program executes the tool
4. the result is sent back to the model

---

## Key concept: Two-step agent pattern

Tool use typically follows this pattern:

1. **Decision step**

   * Model decides: answer or tool call

2. **Execution step**

   * Python executes the tool

3. **Final response**

   * Model generates a user-friendly reply using the tool result

This separation is fundamental to most real-world agents.

---

## Project structure

```text
exercise-03-tool-agent/
├── agent.py
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

---

### 3. Configure environment variables

Copy:

```bash
cp .env.example .env
```

Then fill in:

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

## Available tools

Your agent can use the following tools:

* `get_current_time()`
* `calculate(expression)`
* `save_note(text)`

These are implemented in `tools.py`.

---

## How it works (high level)

Each user request follows this flow:

1. User input
2. Model decides:

   * `"answer"` → respond directly
   * `"tool_call"` → call a tool
3. If tool is used:

   * Python executes the function
   * Result is sent back to the model
4. Model produces final response

---

## Your tasks

### Task 1 – Run the agent

Verify that:

* normal questions are answered directly
* tool-based questions trigger tool usage

---

### Task 2 – Test all tools

Try at least one example per tool:

```text
What time is it?
Calculate 144 / 12 + 7
Save a note saying call Alice tomorrow
```

---

### Task 3 – Inspect the decision step

Print the model decision before execution:

```python
print(json.dumps(decision, indent=2))
```

Look at:

* `mode`
* `tool_name`
* `tool_input`

---

### Task 4 – Trace the full flow

Understand the sequence:

```text
User → Model (decision) → Tool → Model (final answer)
```

---

### Task 5 – Modify behavior

Try:

* Make the agent prefer tools more aggressively
* Add stricter validation for tool inputs
* Change how results are presented

---

## Important concept: Tools vs. LLM

Language models are good at:

* reasoning
* generating text

Tools are good at:

* precise computation
* accessing real data
* performing actions

Combining both gives you much more powerful systems.

---

## Optional challenges

If you finish early, try one of these:

* Add a new tool:

  * `read_notes()`
  * `clear_notes()`
* Log every tool call to a file
* Prevent duplicate notes
* Add confirmation before saving notes
* Add a fake weather tool

---

## Key takeaway

An agent becomes truly useful when it can:

* reason (LLM)
* act (tools)
* iterate (loop + memory)

This exercise combines all three.
