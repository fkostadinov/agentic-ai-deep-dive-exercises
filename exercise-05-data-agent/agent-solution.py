import json
import os
import sqlite3
from typing import Any

from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()

FOUNDRY_ENDPOINT = os.environ["FOUNDRY_ENDPOINT"].rstrip("/")
FOUNDRY_API_KEY = os.environ["FOUNDRY_API_KEY"]
FOUNDRY_MODEL = os.environ["FOUNDRY_MODEL"]

client = OpenAI(
    api_key=FOUNDRY_API_KEY,
    base_url=FOUNDRY_ENDPOINT,
)


def create_database() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
    )

    cur.executemany(
        "INSERT INTO customers (id, name, city) VALUES (?, ?, ?)",
        [
            (1, "Alice", "Zurich"),
            (2, "Bob", "Bern"),
            (3, "Charlie", "Zurich"),
            (4, "Diana", "Basel"),
        ],
    )

    cur.executemany(
        "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
        [
            (1, "Laptop", 1500.0),
            (2, "Mouse", 25.0),
            (3, "Keyboard", 70.0),
            (4, "Monitor", 320.0),
        ],
    )

    cur.executemany(
        "INSERT INTO orders (id, customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, 1, 1, "2026-03-01"),
            (2, 1, 2, 2, "2026-03-02"),
            (3, 2, 4, 1, "2026-03-02"),
            (4, 3, 3, 1, "2026-03-03"),
            (5, 3, 2, 3, "2026-03-03"),
            (6, 4, 1, 1, "2026-03-04"),
        ],
    )

    conn.commit()
    return conn


def get_schema(conn: sqlite3.Connection) -> str:
    cur = conn.cursor()
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    lines = []
    for table_row in tables:
        table_name = table_row[0]
        columns = cur.execute(f"PRAGMA table_info({table_name})").fetchall()
        column_defs = ", ".join(f"{col['name']} {col['type']}" for col in columns)
        lines.append(f"{table_name}({column_defs})")

    return "\n".join(lines)


def validate_sql(sql: str) -> None:
    normalized = sql.strip().lower()

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "pragma",
    ]

    if not normalized.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in normalized.rstrip(";"):
        raise ValueError("Multiple statements are not allowed.")

    if "--" in normalized or "/*" in normalized or "*/" in normalized:
        raise ValueError("SQL comments are not allowed.")

    for keyword in forbidden_keywords:
        if keyword in normalized:
            raise ValueError(f"Forbidden keyword detected: {keyword}")


def execute_sql(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    cur = conn.cursor()
    rows = cur.execute(sql).fetchall()
    return [dict(row) for row in rows]


def generate_sql_with_llm(
    client: OpenAI,
    question: str,
    schema: str,
    conversation_history: list[dict[str, str]],
) -> str:
    system_prompt = f"""
You are a careful SQLite text-to-SQL assistant.

Your task:
- Translate the user's question into exactly one SQLite SELECT statement.
- Only use tables and columns from this schema.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, PRAGMA, ATTACH, or multiple statements.
- Return only raw SQL, no markdown, no explanation.
- The output must start with SELECT.
- Do not include markdown, code fences, or backticks.
- Do not include explanations or comments.
- Do not prefix with "sql".
- Output must be valid SQLite SQL only.

Schema:
{schema}
""".strip()

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})

    response = client.responses.create(
        model=FOUNDRY_MODEL,
        input=messages,
    )

    return response.output_text.strip()


def summarize_results_with_llm(
    client: OpenAI,
    question: str,
    sql: str,
    rows: list[dict[str, Any]],
) -> str:
    prompt = f"""
The user asked:
{question}

The executed SQL was:
{sql}

The SQL result rows are:
{json.dumps(rows, ensure_ascii=False, indent=2)}

Write a short, helpful natural-language answer for the user.
""".strip()

    response = client.responses.create(
        model=FOUNDRY_MODEL,
        input=prompt,
    )
    return response.output_text.strip()


def print_rows(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("(no rows)")
        return

    headers = list(rows[0].keys())
    widths = {h: len(h) for h in headers}

    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(row[h])))

    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    separator = "-+-".join("-" * widths[h] for h in headers)

    print(header_line)
    print(separator)

    for row in rows:
        print(" | ".join(str(row[h]).ljust(widths[h]) for h in headers))


def extract_sql(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


def run_agent_loop(client: OpenAI, conn: sqlite3.Connection, schema: str, conversation_history):
    while True:
        question = input("User> ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            sql_raw = generate_sql_with_llm(client, question, schema, conversation_history)
            sql = extract_sql(sql_raw)

            print("\nGenerated SQL:")
            print(sql)

            validate_sql(sql)

            confirm = input("\nExecute this query? (y/n) ").strip().lower()
            if confirm != "y":
                print("Query not executed.\n")
                continue

            rows = execute_sql(conn, sql)

            print("\nRaw result:")
            print_rows(rows)

            answer = summarize_results_with_llm(client, question, sql, rows)
            print("\nAgent answer:")
            print(answer)
            print()

            conversation_history.append({"role": "user", "content": question})
            conversation_history.append({"role": "assistant", "content": answer})

        except Exception as exc:
            print(f"\nError: {exc}\n")



def main() -> None:

    conn = create_database()
    schema = get_schema(conn)

    print("Data agent started. Type 'exit' to quit.\n")

    conversation_history: list[dict[str, str]] = []
    run_agent_loop(client, conn, schema, conversation_history)


if __name__ == "__main__":
    main()