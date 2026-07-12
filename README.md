# EduRAG Assistant

An AI-powered academic document assistant built as a multi-tenant, **agentic RAG system** with LangGraph, using Retrieval-Augmented Generation to answer questions, summarize, quiz, and explain content from uploaded PDFs — with authenticated, per-user workspaces.

🚀 **Live Demo:** https://edu-rag-assistant.vercel.app/

Users sign up, get their own isolated document workspace, and can upload academic PDFs, ask questions, generate summaries, create quizzes, extract key topics, and receive simplified explanations based on their own document content — through both a web UI and an MCP server compatible with Claude Desktop.

---

## Features

### Authentication & Per-User Workspaces
- JWT-based signup/login, with passwords hashed via bcrypt
- Each user gets their own isolated Chroma vector collection — documents, retrieval, and chat are fully scoped per account
- Verified via cross-user testing: one account's documents are never visible or retrievable by another

### PDF Upload & Indexing
- Upload academic PDF documents
- Automatic text extraction
- Vector database indexing, scoped to the authenticated user

<img width="1920" height="979" alt="Screenshot (408)" src="https://github.com/user-attachments/assets/16e238fd-9623-4b7d-9cb0-0f54d6d988e9" />
<img width="1920" height="1017" alt="Screenshot (410)" src="https://github.com/user-attachments/assets/f63d7b1b-3283-4c0a-bfc9-236f1e4f2a3c" />



### Agentic Routing & Grounding
- LangGraph-based intent classification routes free-text queries to the correct handler (Q&A, summary, quiz, topics, explain) without hardcoded button mapping
- Relevance-gated grounding check filters retrieved context by distance threshold before generation, blocking the LLM call entirely on off-topic questions to prevent hallucination
- Few-shot prompted, temperature-0 classifier for reliable intent detection

### RAG Question Answering
- Ask questions directly from uploaded PDFs
- Context-aware, grounded responses
- Source citation support

<img width="1920" height="1017" alt="Screenshot (411)" src="https://github.com/user-attachments/assets/053bbaf6-06a5-4b58-837f-720e24e6b784" />
<img width="1920" height="1007" alt="Screenshot (412)" src="https://github.com/user-attachments/assets/98bcf4a5-446a-452a-bf5a-a2357a24df12" />




### AI Learning Tools
- Document Summarization
- Quiz Generation
- Key Topic Extraction
- Explain Simply Mode

<img width="1920" height="1014" alt="Screenshot (413)" src="https://github.com/user-attachments/assets/707d20a6-1a7f-40f9-a017-d00421c155cf" />
<img width="1920" height="1004" alt="Screenshot (414)" src="https://github.com/user-attachments/assets/7670bfaa-dc56-4c8c-904e-64484d6be665" />
<img width="1920" height="1011" alt="Screenshot (415)" src="https://github.com/user-attachments/assets/adc1c7a6-ba44-43e0-8470-4452d6c4fbf6" />




### Insights Dashboard
- Per-user usage stats — questions asked, average response time, PDFs uploaded, eval pass rate — pulled live from Langfuse and filtered by authenticated user
- Personal document history (filename, chunk count, upload timestamp), backed by a SQLite records table rather than reconstructed from trace data

<img width="1920" height="1007" alt="Screenshot (416)" src="https://github.com/user-attachments/assets/db93bf55-26d6-4e23-af2f-d1f678a5519b" />


### Observability & Evaluation
- Full request tracing via Langfuse — intent classification, retrieval distances, and generation captured per request, tagged by user
- Regression eval harness (`eval.py`) with categorized test cases (in-document, off-topic, borderline, intent-routing), scored and logged to Langfuse

### MCP Server
- EduRAG's capabilities exposed as MCP tools (`ask_question`, `summarize_document`, `generate_quiz`, `extract_topics`, `explain_simply`)
- Verified working with Claude Desktop as an MCP client
- Reuses the same agentic graph as the web app — no duplicated logic

### User Experience
- Chat history
- Copy answer functionality
- Download answer as text file
- Source references
- Clear chat option

---

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Axios
- React Context (auth state)

### Backend
- FastAPI
- Python
- LangChain
- LangGraph
- SQLAlchemy + SQLite (users, documents)
- PyJWT + bcrypt (authentication)

### AI & RAG
- LangChain
- LangGraph
- Groq API
- Llama 3.3 70B
- ChromaDB (per-user collections)
- HuggingFace Embeddings
- Sentence Transformers

### Observability & Tooling
- Langfuse (tracing, scoring, per-user filtering)
- Model Context Protocol (MCP)

---

## Project Structure
backend
├── app.py
├── rag.py
├── retrieval.py
├── graph.py
├── auth.py
├── database.py
├── mcp_server.py
├── eval.py
├── test_vector_db.py
├── uploads
├── vector_db

frontend
├── src
│   ├── components
│   ├── context
│   ├── services
│   ├── types
│   └── App.tsx

---

## Installation

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### MCP Server (optional, for use with Claude Desktop)
```bash
cd backend
python mcp_server.py
```
Add to your Claude Desktop config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "edurag": {
      "command": "path/to/venv/Scripts/python.exe",
      "args": ["path/to/backend/mcp_server.py"]
    }
  }
}
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| POST /auth/signup | Create a new account |
| POST /auth/login | Log in, receive JWT |
| GET /auth/me | Get current authenticated user |
| POST /upload | Upload PDF (authenticated, scoped to user) |
| POST /ask | Ask questions (fixed intent, authenticated) |
| POST /summary | Generate summary (authenticated) |
| POST /quiz | Generate quiz (authenticated) |
| POST /topics | Extract key topics (authenticated) |
| POST /explain | Explain simply (authenticated) |
| POST /agent | Free-text query with agentic intent routing (authenticated) |
| GET /stats | Per-user usage stats from Langfuse (authenticated) |
| GET /documents | Per-user document upload history (authenticated) |

---

## Running Evals

```bash
cd backend
python eval.py
```
Runs a categorized regression test set against the live agentic pipeline and logs pass/fail scores to Langfuse.

---

## Future Improvements
- Hybrid search (keyword + vector) with cross-encoder re-ranking
- Multi-document support within a single workspace (cross-document comparison queries)
- Persistent storage for SQLite/vector data on Railway via volumes
- Export to PDF
- Chat session persistence across devices

---

## Deployment
**Frontend:** Vercel
**Backend:** Railway
**Vector Database:** ChromaDB (per-user collections)
**Relational Database:** SQLite (users, documents)
**LLM:** Groq Cloud (Llama 3.3 70B)
**Observability:** Langfuse Cloud

---

## Author
Fahad Irfan — Full-Stack AI Developer
GitHub: https://github.com/Fahad-12345/
Portfolio: https://fahadirfan.vercel.app/
