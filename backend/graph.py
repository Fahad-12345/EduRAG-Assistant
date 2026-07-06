# graph.py
import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from retrieval import retrieve_context
from langfuse import observe, get_client

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

classifier_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0,
)

PROMPTS = {
    "qa": """You are an AI University Assistant.
Answer the student's question using only the context below.
If the answer is not available in the context, say:
"I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:""",

    "summary": """Summarize this uploaded document in clear bullet points.
Keep it useful for a university student.

Context:
{context}

Answer:""",

    "quiz": """Generate 10 quiz questions from the uploaded document.

Format:
1. Question
A) Option A
B) Option B
C) Option C
D) Option D
Answer: Correct option

Context:
{context}

Answer:""",

    "topics": """Extract the main key topics covered in the uploaded document.

Format:
- Topic 1
- Topic 2

Context:
{context}

Answer:""",

    "explain": """Explain the uploaded document in simple, easy-to-understand language
for a university student seeing this topic for the first time.

Context:
{context}

Answer:""",
}


class GraphState(TypedDict):
    question: str
    intent: str
    context: str
    docs: List
    answer: str
    sources: List[dict]


@observe(name="classify-intent")
def classify_intent_node(state: GraphState) -> GraphState:
    """Routes free-text input to the right prompt template.
    Button-triggered calls will set intent directly and skip this node."""
    question = state["question"]

    classification_prompt = f"""Classify this request into exactly one category: qa, summary, quiz, topics, explain

Rules:
- "qa" = the user is asking a specific factual question, even if phrased as "tell me about X" or "what is X" — default to qa unless it's clearly a command.
- "summary" = ONLY if the user explicitly asks to summarize the document (e.g. "summarize this", "give me a summary").
- "quiz" = ONLY if the user explicitly asks for a quiz or test questions.
- "topics" = ONLY if the user explicitly asks for topics or key themes (e.g. "what topics are covered").
- "explain" = ONLY if the user explicitly asks for a simple/easy explanation of the whole document (e.g. "explain this simply", "explain like I'm new").

Examples:
"What is Agile development?" -> qa
"Tell me about risk in software projects" -> qa
"What is throwaway prototyping?" -> qa
"Summarize this" -> summary
"Give me a quiz" -> quiz
"What are the key topics?" -> topics
"Explain this simply" -> explain

Request: "{question}"

Reply with only the category word, nothing else."""

    result = classifier_llm.invoke(classification_prompt).content.strip().lower()

    valid_intents = {"qa", "summary", "quiz", "topics", "explain"}
    state["intent"] = result if result in valid_intents else "qa"

    get_client().update_current_span(
        input=question,
        output=state["intent"],
    )

    return state

@observe(name="retrieve-context")
def retrieve_node(state: GraphState) -> GraphState:
    if state["intent"] == "qa":
        result = retrieve_context(state["question"], apply_filter=True)
    else:
        # summary/quiz/topics/explain: fetch broadly, no relevance filtering
        result = retrieve_context(state["intent"], k=8, apply_filter=False)
    state["docs"] = result["docs"]
    state["context"] = result["context"]
    get_client().update_current_span(
        metadata={"num_docs_retrieved": len(result["docs"])}
    )
    return state

def grounding_check(state: GraphState) -> str:
    """Conditional edge: skip the LLM entirely if retrieval found nothing.
    This is the hallucination-prevention step."""
    if not state["docs"] or not state["context"].strip():
        return "not_found"
    return "generate"


def not_found_node(state: GraphState) -> GraphState:
    state["answer"] = "I could not find this information in the uploaded document."
    state["sources"] = []
    return state


@observe(name="generate-answer", as_type="generation")
def generate_node(state: GraphState) -> GraphState:
    prompt_template = PROMPTS[state["intent"]]
    prompt = prompt_template.format(context=state["context"], question=state["question"])

    response = llm.invoke(prompt)
    answer_text = response.content.strip()

    not_found_phrases = [
        "i could not find this information in the uploaded document",
        "could not find this information",
        "not available in the context",
    ]

    if any(p in answer_text.lower() for p in not_found_phrases):
        state["answer"] = answer_text
        state["sources"] = []
        return state

    sources = []
    for doc in state["docs"]:
        source = doc.metadata.get("source", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")
        item = {"file": os.path.basename(source), "page": page + 1 if isinstance(page, int) else page}
        if item not in sources:
            sources.append(item)

    state["answer"] = answer_text
    state["sources"] = sources
    get_client().update_current_span(
        input=prompt,
        output=answer_text,
        metadata={"intent": state["intent"]},
    )
    return state
def route_entry(state: GraphState) -> str:
    """If intent is already set (button click), skip classification."""
    return "retrieve" if state["intent"] else "classify_intent"


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("not_found", not_found_node)

    workflow.set_conditional_entry_point(
        route_entry,
        {"classify_intent": "classify_intent", "retrieve": "retrieve"}
    )
    workflow.add_edge("classify_intent", "retrieve")
    workflow.add_conditional_edges(
        "retrieve",
        grounding_check,
        {"generate": "generate", "not_found": "not_found"}
    )
    workflow.add_edge("generate", END)
    workflow.add_edge("not_found", END)

    return workflow.compile()

agent_graph = build_graph()

@observe(name="edurag-agent-run")
def run_agent(question: str, intent: str = None):
    initial_state = {
        "question": question,
        "intent": intent or "",
        "context": "",
        "docs": [],
        "answer": "",
        "sources": [],
    }
    result = agent_graph.invoke(initial_state)
    return {"answer": result["answer"], "sources": result["sources"]}
    