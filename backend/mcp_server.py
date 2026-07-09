# mcp_server.py
from mcp.server.fastmcp import FastMCP
from graph import run_agent

mcp = FastMCP("EduRAG Assistant")

# MCP clients (e.g. Claude Desktop) aren't authenticated web users —
# they operate under a fixed identity scoped to its own Chroma collection.
MCP_USER_ID = "mcp-client"


@mcp.tool()
def ask_question(question: str) -> str:
    """Ask a question about the currently uploaded document."""
    response = run_agent(question, user_id=MCP_USER_ID, intent="qa")
    return response["answer"]


@mcp.tool()
def summarize_document() -> str:
    """Generate a bullet-point summary of the currently uploaded document."""
    response = run_agent("Summarize the document", user_id=MCP_USER_ID, intent="summary")
    return response["answer"]


@mcp.tool()
def generate_quiz() -> str:
    """Generate a 10-question multiple-choice quiz from the currently uploaded document."""
    response = run_agent("Generate a quiz", user_id=MCP_USER_ID, intent="quiz")
    return response["answer"]


@mcp.tool()
def extract_topics() -> str:
    """Extract the main key topics covered in the currently uploaded document."""
    response = run_agent("Extract topics", user_id=MCP_USER_ID, intent="topics")
    return response["answer"]


@mcp.tool()
def explain_simply() -> str:
    """Explain the currently uploaded document in simple, easy-to-understand language."""
    response = run_agent("Explain simply", user_id=MCP_USER_ID, intent="explain")
    return response["answer"]


if __name__ == "__main__":
    mcp.run(transport="stdio")