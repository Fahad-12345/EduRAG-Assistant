from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag import ingest_pdf
from graph import run_agent

from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://edu-rag-assistant.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI University Assistant Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = ingest_pdf(file_path)

    return {
        "status": "success",
        "chunks": chunks
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    return run_agent(request.question, intent="qa")

@app.post("/summary")
def summary():
    return run_agent("Summarize the document", intent="summary")

@app.post("/quiz")
def quiz():
    return run_agent("Generate a quiz", intent="quiz")

@app.post("/topics")
def topics():
    return run_agent("Extract topics", intent="topics")

@app.post("/explain")
def explain():
    return run_agent("Explain simply", intent="explain")

# NEW — genuinely agentic endpoint, no fixed intent, model decides
@app.post("/agent")
def agent(request: QuestionRequest):
    return run_agent(request.question)
    
