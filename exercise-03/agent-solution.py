import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import calculate, get_current_time, save_note


load_dotenv()

FOUNDRY_ENDPOINT = os.environ["FOUNDRY_ENDPOINT"].rstrip("/")
FOUNDRY_API_KEY = os.environ["FOUNDRY_API_KEY"]
FOUNDRY_MODEL = os.environ["FOUNDRY_MODEL"]

client = OpenAI(
    api_key=FOUNDRY_API_KEY,
    base_url=FOUNDRY_ENDPOINT,
)

TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "save_note": save_note,
}

SYSTEM_PROMPT = """
You are a simple software agent with access to tools.

You must always respond in valid JSON with exactly this schema:
{
  "mode": "answer" or "tool_call",
  "response_to_user": "direct reply if no tool is needed, otherwise empty string",
  "tool_name": "tool name or empty string",
  "tool_input": {},
  "reason": "short explanation"
}

Available tools:
1. get_current_time()
   Use when the user asks for the current time.

2. calculate(expression)
   Use when the user asks for a mathematical calculation.

3. save_note(text)
   Use when the user asks to save a short note.

Rules:
- If you can answer directly without a tool, use mode = "answer".
- If a tool is needed, use mode = "tool_call".
- Only use the available tools.
- tool_input must be a JSON object.
- Do not use markdown.
"""

FINAL_RESPONSE_PROMPT = """
You are a helpful software agent.

You have already used a tool.
Based on the original user request and the tool result, respond to the user clearly and concisely.

Always respond in valid JSON with exactly this schema:
{
  "response_to_user": "final reply to the user"
}

Do not use markdown.
"""


def call_model(messages):
    response = client.chat.completions.create(
        model=FOUNDRY_MODEL,
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def execute_tool(tool_name, tool_input):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]
    return tool(**tool_input)


def run_agent_loop(history):
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter something.")
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if user_input.lower() == "reset":
            history[:] = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Memory cleared.")
            continue

        if user_input.lower() == "history":
            print(json.dumps(history, indent=2, ensure_ascii=False))
            continue

        history.append({"role": "user", "content": user_input})

        try:
            decision = call_model(history)
        except Exception as e:
            print(f"Error during model decision: {e}")
            history.pop()
            continue

        if decision["mode"] == "answer":
            print("\nAgent")
            print("-" * 40)
            print(decision["response_to_user"])

            history.append({
                "role": "assistant",
                "content": json.dumps(decision, ensure_ascii=False)
            })
            continue

        if decision["mode"] == "tool_call":
            tool_name = decision["tool_name"]
            tool_input = decision["tool_input"]

            try:
                tool_result = execute_tool(tool_name, tool_input)
            except Exception as e:
                print("\nAgent")
                print("-" * 40)
                print(f"Tool execution failed: {e}")
                continue

            follow_up_messages = [
                {"role": "system", "content": FINAL_RESPONSE_PROMPT},
                {"role": "user", "content": user_input},
                {
                    "role": "assistant",
                    "content": json.dumps(decision, ensure_ascii=False)
                },
                {
                    "role": "user",
                    "content": f"Tool result: {tool_result}"
                },
            ]

            try:
                final_result = call_model(follow_up_messages)
            except Exception as e:
                print(f"Error during final response generation: {e}")
                continue

            print("\nAgent")
            print("-" * 40)
            print(final_result["response_to_user"])

            history.append({
                "role": "assistant",
                "content": json.dumps(
                    {
                        "decision": decision,
                        "tool_result": tool_result,
                        "final_result": final_result,
                    },
                    ensure_ascii=False
                )
            })
            continue

        print("\nAgent")
        print("-" * 40)
        print("The model returned an unknown mode.")


def main():
    print("Exercise 03 - Tool-Using Agent")
    print("Commands: history, reset, exit\n")

    history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("Hi, I am your helpful assistant. I can tell you the time, " \
        "perform simple mathematical calculations, or save some " \
        "important notes to disk.\n" \
        "Type EXIT or QUIT to abort the program.\n" \
        "Type HISTORY to see the entire chat history.\n" \
        "Type RESET to clear the entire chat history."
        )

    run_agent_loop(history)


if __name__ == "__main__":
    main()