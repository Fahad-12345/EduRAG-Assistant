# EduRAG Assistant

An AI-powered academic document assistant built as an **agentic RAG system** with LangGraph, using Retrieval-Augmented Generation to answer questions, summarize, quiz, and explain content from uploaded PDFs.

🚀 **Live Demo:** https://edu-rag-assistant.vercel.app/

Users can upload academic PDFs, ask questions, generate summaries, create quizzes, extract key topics, and receive simplified explanations based on document content — through both a web UI and an MCP server compatible with Claude Desktop.

---

## Features

### PDF Upload & Indexing
- Upload academic PDF documents
- Automatic text extraction
- Vector database indexing

<img width="1920" height="1014" alt="home" src="https://github.com/user-attachments/assets/21c1cd79-984e-4bcf-8572-69b30ca87203" />

### Agentic Routing & Grounding
- LangGraph-based intent classification routes free-text queries to the correct handler (Q&A, summary, quiz, topics, explain) without hardcoded button mapping
- Relevance-gated grounding check filters retrieved context by distance threshold before generation, blocking the LLM call entirely on off-topic questions to prevent hallucination
- Few-shot prompted, temperature-0 classifier for reliable intent detection

### RAG Question Answering
- Ask questions directly from uploaded PDFs
- Context-aware, grounded responses
- Source citation support

<img width="1920" height="1080" alt="ask_question" src="https://github.com/user-attachments/assets/64a2c42c-ea0b-43b3-a8d4-47c254c81d5a" />
<img width="1920" height="1080" alt="answer_question" src="https://github.com/user-attachments/assets/343ddc23-cb72-49b6-b89d-15b917e19153" />

### AI Learning Tools
- Document Summarization
- Quiz Generation
- Key Topic Extraction
- Explain Simply Mode

<img width="1920" height="1080" alt="summary" src="https://github.com/user-attachments/assets/6afac300-a5e9-4e00-af04-a5152ee8a7a6" />
<img width="1920" height="1080" alt="quiz_generation" src="https://github.com/user-attachments/assets/5020f061-bbd2-4543-aa23-402258928dab" />
<img width="1920" height="1080" alt="key_topics" src="https://github.com/user-attachments/assets/29b40d84-f7e0-4757-bf49-5832773e8cef" />
<img width="1920" height="1080" alt="explain_simply" src="https://github.com/user-attachments/assets/a737b32b-acb9-4934-b4b3-db59b82f27a9" />

### Observability & Evaluation
- Full request tracing via Langfuse — intent classification, retrieval distances, and generation captured per request
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

### Backend
- FastAPI
- Python
- LangChain
- LangGraph

### AI & RAG
- LangChain
- LangGraph
- Groq API
- Llama 3.3 70B
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers

### Observability & Tooling
- Langfuse (tracing, scoring)
- Model Context Protocol (MCP)

---

## Project Structure
backend
├── app.py
├── rag.py
├── retrieval.py
├── graph.py
├── mcp_server.py
├── eval.py
├── test_vector_db.py
├── uploads
├── vector_db

frontend
├── src
│   ├── components
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
| POST /upload | Upload PDF |
| POST /ask | Ask questions (fixed intent) |
| POST /summary | Generate summary |
| POST /quiz | Generate quiz |
| POST /topics | Extract key topics |
| POST /explain | Explain simply |
| POST /agent | Free-text query with agentic intent routing |

---

## Running Evals

```bash
cd backend
python eval.py
```
Runs a categorized regression test set against the live agentic pipeline and logs pass/fail scores to Langfuse.

---

## Future Improvements
- Multi-document support
- User authentication
- Hybrid search (keyword + vector)
- Re-ranking step before generation
- Export to PDF
- Chat session persistence

---

## Deployment
**Frontend:** Vercel
**Backend:** Railway
**Vector Database:** ChromaDB
**LLM:** Groq Cloud (Llama 3.3 70B)
**Observability:** Langfuse Cloud

---

## Author
Fahad Irfan — Full-Stack AI Developer
GitHub: https://github.com/Fahad-12345/
Portfolio: https://fahadirfan.vercel.app/
