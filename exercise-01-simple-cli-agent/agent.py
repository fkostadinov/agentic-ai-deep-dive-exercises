import json
import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()

FOUNDRY_ENDPOINT = os.environ["FOUNDRY_ENDPOINT"].rstrip("/")
FOUNDRY_API_KEY = os.environ["FOUNDRY_API_KEY"]
FOUNDRY_API_VERSION = os.environ.get("FOUNDRY_API_VERSION", "2024-05-01-preview")
FOUNDRY_MODEL = os.environ["FOUNDRY_MODEL"]

SYSTEM_PROMPT = """
You are a simple software agent.

Your task is to help the user achieve a goal.
Always respond in valid JSON and nothing else.

Use exactly this schema:
{
  "goal": "short restatement of the user's goal",
  "plan": ["step 1", "step 2", "step 3"],
  "next_action": "the single best next action"
}

Rules:
- Keep the plan practical and concise.
- Return 3 to 5 steps.
- Do not use markdown.
"""


def call_model(user_goal: str) -> dict[str, Any]:
    url = f"{FOUNDRY_ENDPOINT}/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FOUNDRY_API_KEY}",
    }

    # Hint: Certain types of "reasoning models" do not support all standard payload parameters.
    # More info: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning
    payload = {
        "model": FOUNDRY_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"My goal is: {user_goal}"},
        ],
        # "temperature": 1, # This parameter is not supported by gpt-5-nano
        # "max_tokens": 700, # This parameter is not supported by gpt-5-nano
        "response_format": {"type": "json_object"},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    # To print the server's JSON response, uncomment the following lines:
    """
    print()
    print("-" * 40)
    print("Server response:")
    print(json.dumps(data, indent=2))
    print("-" * 40)
    print()
    """

    content = data["choices"][0]["message"]["content"]

    return json.loads(content)


def main() -> None:
    print("Exercise 01 - Simple CLI Agent")
    print("Enter a goal for the agent.\n")

    user_goal = input("Goal: ").strip()
    if not user_goal:
        print("No goal entered.")
        return

    try:
        result = call_model(user_goal)
    except requests.HTTPError as e:
        print("\nHTTP error")
        print(e)
        if e.response is not None:
            print(e.response.text)
        return
    except Exception as e:
        print(f"\nError: {e}")
        return

    print("\nAgent output")
    print("-" * 40)
    print(f"Goal: {result['goal']}\n")

    print("Plan:")
    for i, step in enumerate(result["plan"], start=1):
        print(f"{i}. {step}")

    print(f"\nNext action: {result['next_action']}")


if __name__ == "__main__":
    main()