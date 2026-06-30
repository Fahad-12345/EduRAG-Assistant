from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag import (
    ingest_pdf,
    ask_question,
    generate_summary,
    generate_quiz,
    generate_topics,
    explain_simply
)
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://edurag-assistant-production.up.railway.app"],
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
    response = ask_question(request.question)

    return response
@app.post("/summary")
def summary():
    response = generate_summary()
    return response
@app.post("/quiz")
def quiz():
    response = generate_quiz()
    return response
@app.post("/topics")
def topics():
    response = generate_topics()
    return response
@app.post("/explain")
def explain():
    response = explain_simply()
    return response