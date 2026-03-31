import json
import os

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

SYSTEM_PROMPT = """
You are a simple stateful software agent.

You help the user over multiple turns.
Always respond in valid JSON and nothing else.

Use exactly this schema:
{
  "goal": "short restatement of the user's current goal",
  "mode": "answer" or "follow_up",
  "response_to_user": "the actual reply for the user",
  "plan": ["step 1", "step 2"],
  "next_action": "what should happen next, or empty string if nothing is needed"
}

Rules:
- If the user asks for something you can directly provide now, do it immediately.
- In that case, set "mode" to "answer".
- Only set "mode" to "follow_up" if the task genuinely needs more interaction, clarification, or multiple steps.
- "response_to_user" should always contain the main reply to the user.
- Keep "plan" concise and practical.
- If no real plan is needed, return an empty list.
- If no next action is needed, return an empty string.
- Do not use markdown.
"""


def call_model(messages):
    response = client.chat.completions.create(
        model=FOUNDRY_MODEL,
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)


def print_agent_response(result):
    print("\nAgent")
    print("-" * 40)
    print(result["response_to_user"])

    if result["plan"]:
        print("\nPlan:")
        for i, step in enumerate(result["plan"], start=1):
            print(f"{i}. {step}")

    if result["mode"] == "follow_up" and result["next_action"]:
        print(f"\nNext action: {result['next_action']}")


def run_agent_loop(history):
    """
    EXERCISE TASK - IMPLEMENT THIS FUNCTION!

    1. Implement the agent loop as a while loop.

    2. In the agent loop, first obtain the user's command-line input:
       user_input = input("You: ").strip()

    3. If the user input is "exit" or "EXIT" or "quit" or "QUIT" then break
       the while loop.

    4. In each loop iteration, append the user input to the messages history:
       history.append({"role": "user", "content": user_input})

    5. Call the language model service with the entire messages history:
       try:
           result = call_model(history)
       except json.JSONDecodeError:
           print("Invalid JSON from model.")
           history.pop()
           continue
       except Exception as e:
           print(f"Error: {e}")
           history.pop()
           continue
    
    6. Append the model response to the messages history, too:
       history.append({
          "role": "assistant",
          "content": json.dumps(result, ensure_ascii=False)
       })

    7. (Optional) If the user input is "reset" or "RESET", then
       clear the entire messages history and continue the loop:
       history = [{"role": "system", "content": SYSTEM_PROMPT}]

    8. (Optional) If the user types "history" or "HISTORY", THEN
       pretty print the entire messages history as JSON:
       print(json.dumps(history, indent=2, ensure_ascii=False))
    """

    pass


def main():
    print("Exercise 02 - Stateful CLI Agent")
    print("Commands: reset, history, exit\n")

    history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("Hi, how can I help you today?")

    run_agent_loop(history)


if __name__ == "__main__":
    main()