# mcp_server.py
from mcp.server.fastmcp import FastMCP
from graph import run_agent

mcp = FastMCP("EduRAG Assistant")


@mcp.tool()
def ask_question(question: str) -> str:
    """Ask a question about the currently uploaded document. 
    Returns an answer grounded in the document, or a refusal if the answer isn't found."""
    response = run_agent(question, intent="qa")
    return response["answer"]


@mcp.tool()
def summarize_document() -> str:
    """Generate a bullet-point summary of the currently uploaded document."""
    response = run_agent("Summarize the document", intent="summary")
    return response["answer"]


@mcp.tool()
def generate_quiz() -> str:
    """Generate a 10-question multiple-choice quiz from the currently uploaded document."""
    response = run_agent("Generate a quiz", intent="quiz")
    return response["answer"]


@mcp.tool()
def extract_topics() -> str:
    """Extract the main key topics covered in the currently uploaded document."""
    response = run_agent("Extract topics", intent="topics")
    return response["answer"]


@mcp.tool()
def explain_simply() -> str:
    """Explain the currently uploaded document in simple, easy-to-understand language."""
    response = run_agent("Explain simply", intent="explain")
    return response["answer"]


if __name__ == "__main__":
    mcp.run(transport="stdio")