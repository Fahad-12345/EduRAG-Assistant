# EduRAG Assistant

An AI-powered academic document assistant built using Retrieval-Augmented Generation (RAG).

🚀 **Live Demo:** https://edu-rag-assistant.vercel.app/

Users can upload academic PDFs, ask questions, generate summaries, create quizzes, extract key topics, and receive simplified explanations based on document content.

---

## Features

### PDF Upload & Indexing
- Upload academic PDF documents
- Automatic text extraction
- Vector database indexing
  
<img width="1920" height="1014" alt="home" src="https://github.com/user-attachments/assets/21c1cd79-984e-4bcf-8572-69b30ca87203" />


### RAG Question Answering
- Ask questions directly from uploaded PDFs
- Context-aware responses
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
- LangChain
- Groq API
- Llama 3.3 70B
- ChromaDB
- HuggingFace Embeddings
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
---
## Deployment

Frontend:
- Vercel

Backend:
- Railway

Vector Database:
- ChromaDB

LLM:
- Groq Cloud (Llama 3.3 70B)

---

## Author

Fahad Irfan — Full-Stack AI Developer

GitHub: github.com/Fahad-12345
Portfolio: fahadirfan.vercel.app
