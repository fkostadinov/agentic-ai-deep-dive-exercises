from mcp.server.fastmcp import FastMCP
from tools import calculate, get_current_time, save_note

mcp = FastMCP("example-tools")


@mcp.tool()
def get_current_time_tool() -> str:
    return get_current_time()


@mcp.tool()
def calculate_tool(expression: str) -> str:
    return calculate(expression)


@mcp.tool()
def save_note_tool(text: str) -> str:
    return save_note(text)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")