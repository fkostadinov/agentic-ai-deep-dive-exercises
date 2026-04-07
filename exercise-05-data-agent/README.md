# Exercise 05 – Conversational Data Agent (Text-to-SQL)

## Objective

Build a conversational data agent in Python that translates natural-language questions into SQL queries, validates them, executes them against an in-memory SQLite database, and returns both raw results and a natural-language answer.

Unlike previous exercises, this one includes a full agent loop with a language model in the decision-making step.

---

## Learning Goals

By completing this exercise, you will learn:

* How a text-to-SQL data agent works end-to-end
* How to integrate an LLM into an agent loop
* How to retrieve and pass database schema context
* How to validate and safely execute generated SQL
* How to separate generation, validation, and execution
* How to build a conversational loop with memory

---

## Scenario

You are building a small analytics agent for a shop database.

The database contains:

* customers
* products
* orders

A user can ask questions such as:

* "How many customers live in Zurich?"
* "What are the most expensive products?"
* "How many orders did Alice place?"
* "What is the total revenue per customer?"

The agent should:

1. understand the question,
2. generate SQL using an LLM,
3. validate the SQL,
4. optionally ask for confirmation,
5. execute the query,
6. return results and a natural-language answer,
7. continue the conversation in a loop.

---

## Architecture Overview

The agent follows this flow:

User question
→ retrieve schema
→ generate SQL (LLM)
→ sanitize output
→ validate SQL
→ confirm execution
→ execute SQL
→ return raw results
→ summarize results (LLM)
→ continue loop

---

## Files

* `agent.py` – main implementation
* `.env` – environment variables (not committed)
* `requirements.txt` – dependencies

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install openai python-dotenv
```

### 3. Create a `.env` file

```text
FOUNDRY_ENDPOINT=...
FOUNDRY_API_KEY=...
FOUNDRY_MODEL=...
```

Make sure the file is named exactly `.env` and is located in the same directory as `agent.py`.

---

## Running the Agent

```bash
python agent.py
```

Example interaction:

```
User> How many customers live in Zurich?

Generated SQL:
SELECT COUNT(*) FROM customers WHERE city = 'Zurich';

Execute this query? (y/n) y

Raw result:
COUNT(*)
--------
2

Agent answer:
There are 2 customers living in Zurich.
```

---

## Implementation Details

### Key Components

* `create_database()`
  Creates and seeds an in-memory SQLite database.

* `get_schema()`
  Extracts table and column information dynamically.

* `generate_sql_with_llm()`
  Uses the language model to translate natural language into SQL.

* `extract_sql()`
  Cleans model output (e.g. removes markdown or formatting).

* `validate_sql()`
  Ensures only safe, read-only queries are executed.

* `execute_sql()`
  Runs the query against the database.

* `summarize_results_with_llm()`
  Converts raw results into a natural-language answer.

* `run_agent_loop()`
  Implements the interactive agent loop.

---

## Tasks

### Task 1 – Run and Explore

Run the agent and try different queries. Observe:

* generated SQL
* validation behavior
* final answers

---

### Task 2 – Improve SQL Validation

Extend `validate_sql()`:

* reject `UNION` queries
* reject `SELECT *`
* restrict access to known tables only
* optionally estimate query cost

---

### Task 3 – Improve Prompt Robustness

Refine the system prompt:

* enforce strict SQL-only output
* reduce formatting errors
* improve join correctness

---

### Task 4 – Add Retry Logic

If SQL execution fails:

* capture the error
* send the error + SQL back to the LLM
* let the model repair the query

---

### Task 5 – Conversational Context

Enhance multi-turn capability:

Example:

```
User> Show all customers
User> Only those from Zurich
```

You can:

* keep conversation history
* or implement query rewriting

---

### Task 6 – Schema Pruning

Instead of passing the full schema:

* detect relevant tables
* pass only those to the LLM

---

### Task 7 – Logging and Observability

Log:

* user question
* generated SQL
* execution result
* model prompts

---

## Bonus Tasks

* Replace string-based validation with SQL parsing
* Add chart/table visualization
* Support aggregations and grouping explanations
* Add role-based access control (RBAC)
* Track token usage and cost

---

## Notes

* The model output must never be trusted directly
* Always validate and sanitize before execution
* Prompting improves quality, but does not guarantee correctness
* This architecture mirrors real-world data agents

---

## Key Takeaway

A data agent is not just “LLM → SQL”.

It is a controlled system:

* LLM for reasoning
* code for safety and execution
* validation as the critical boundary

This separation is what makes the system reliable.

---
