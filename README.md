# EduRAG Assistant

An AI-powered academic document assistant built using Retrieval-Augmented Generation (RAG).

Users can upload academic PDFs, ask questions, generate summaries, create quizzes, extract key topics, and receive simplified explanations based on document content.

---

## Features

### PDF Upload & Indexing
- Upload academic PDF documents
- Automatic text extraction
- Vector database indexing

### RAG Question Answering
- Ask questions directly from uploaded PDFs
- Context-aware responses
- Source citation support

### AI Learning Tools
- Document Summarization
- Quiz Generation
- Key Topic Extraction
- Explain Simply Mode

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

### AI & RAG
- Ollama
- Mistral
- ChromaDB
- Sentence Transformers

---

## Project Structure

backend
├── app.py
├── rag.py
├── uploads
├── vector_db

frontend
├── src
│ ├── components
│ ├── services
│ ├── types
│ └── App.tsx

---

## Installation

### Backend

```bash
cd backend

python -m venv venv

venvScriptsactivate

pip install -r requirements.txt

uvicorn appapp --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## API Endpoints

 Endpoint  Description 
-----------------------
 POST upload  Upload PDF 
 POST ask  Ask questions 
 POST summary  Generate summary 
 POST quiz  Generate quiz 
 POST topics  Extract key topics 
 POST explain  Explain simply 

---

## Future Improvements

- Multi-document support
- User authentication
- n8n workflow automation
- Export to PDF
- Chat session persistence
- Cloud deployment

---

## Author

Fahad Irfan

Electrical Engineer | AI Developer

LinkedIn https://www.linkedin.com/in/fahad-irfan-83940b162