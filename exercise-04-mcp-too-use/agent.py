import asyncio
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


load_dotenv()

FOUNDRY_ENDPOINT = os.environ["FOUNDRY_ENDPOINT"].rstrip("/")
FOUNDRY_API_KEY = os.environ["FOUNDRY_API_KEY"]
FOUNDRY_MODEL = os.environ["FOUNDRY_MODEL"]

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")

client = OpenAI(
    api_key=FOUNDRY_API_KEY,
    base_url=FOUNDRY_ENDPOINT,
)

SYSTEM_PROMPT = """
You are a simple software agent with access to tools via MCP.

You must always respond in valid JSON with exactly this schema:
{
  "mode": "answer" or "tool_call",
  "response_to_user": "direct reply if no tool is needed, otherwise empty string",
  "tool_name": "tool name or empty string",
  "tool_input": {},
  "reason": "short explanation"
}

Available tools:
1. get_current_time_tool()
   Use when the user asks for the current time.

2. calculate_tool(expression)
   Use when the user asks for a mathematical calculation.

3. save_note_tool(text)
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
        #temperature=0.2, # This parameter is not supported by gpt-5-nano
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


async def call_mcp_tool(session, tool_name, tool_input):
    result = await session.call_tool(tool_name, arguments=tool_input)

    if hasattr(result, "content") and result.content:
        parts = []
        for item in result.content:
            text = getattr(item, "text", None)
            if text is not None:
                parts.append(text)
            else:
                parts.append(str(item))
        return "\n".join(parts)

    return str(result)


def print_agent_response(text):
    print("\nAgent")
    print("-" * 40)
    print(text)


async def run_agent_loop(history, session):
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

        if user_input.lower() == "tools":
            tools = await session.list_tools()
            print("\nAvailable MCP tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            decision = call_model(history)
        except Exception as e:
            print(f"Error during model decision: {e}")
            history.pop()
            continue

        if decision["mode"] == "answer":
            print_agent_response(decision["response_to_user"])
            history.append(
                {"role": "assistant", "content": json.dumps(decision, ensure_ascii=False)}
            )
            continue

        if decision["mode"] == "tool_call":
            tool_name = decision["tool_name"]
            tool_input = decision["tool_input"]

            try:
                # GOAL: Execute the tool asynchronously with the provided tool inputs.
                # YOUR TASK: Execute the tool asynchronously providing 1) session,
                # 2) tool_name and 3) tool_input as arguments. Store the returned
                # response in a variable called tool_result.
                # --->
                tool_result = await () # YOUR CODE HERE
                # <---  
            except Exception as e:
                print_agent_response(f"Tool execution failed: {e}")
                history.pop()
                continue

            follow_up_messages = [
                {"role": "system", "content": FINAL_RESPONSE_PROMPT},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": json.dumps(decision, ensure_ascii=False)},
                {"role": "user", "content": f"Tool result: {tool_result}"},
            ]

            try:
                final_result = call_model(follow_up_messages)
            except Exception as e:
                print(f"Error during final response generation: {e}")
                history.pop()
                continue

            print_agent_response(final_result["response_to_user"])

            history.append(
                {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "decision": decision,
                            "tool_result": tool_result,
                            "final_result": final_result,
                        },
                        ensure_ascii=False,
                    ),
                }
            )
            continue

        print_agent_response("The model returned an unknown mode.")
        history.pop()


async def main():
    print("Exercise 04 - MCP Tool-Using Agent over HTTP")
    print(f"MCP server: {MCP_SERVER_URL}")
    print("Commands: history, reset, tools, exit\n")

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Connect to the MCP server via streamable http.
    # Note that await streamable_http_client returns a triplet
    # (read_stream, write_strea, extra_value)
    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        
        # Create an MCP client session
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()

            # Obtain a list of tools available with the server
            tools = await session.list_tools()
            print("Connected to MCP server.")
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # Start the agent loop
            await run_agent_loop(history, session)


if __name__ == "__main__":
    asyncio.run(main())