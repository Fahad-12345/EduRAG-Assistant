from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from rag import ingest_pdf, delete_document
from graph import run_agent
from langfuse import observe, get_client, propagate_attributes
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, User, Document
from auth import hash_password, verify_password, create_token, get_current_user
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")


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
    document_ids: list[str] | None = None


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.get("/")
def home():
    return {
        "message": "AI University Assistant Running"
    }


# ---------- Auth routes ----------

@app.post("/auth/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=request.email, hashed_password=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id)
    return {"token": token, "email": user.email}


@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(user.id)
    return {"token": token, "email": user.email}


@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "id": current_user.id}


# ---------- Document/chat routes — now multi-document aware ----------

@app.post("/upload")
@observe(name="pdf-upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    with propagate_attributes(user_id=current_user.id):
        # Create the Document row first so we have a real ID to tag chunks with
        document = Document(user_id=current_user.id, filename=file.filename, chunks=0)
        db.add(document)
        db.commit()
        db.refresh(document)

        file_path = os.path.join(UPLOAD_FOLDER, f"{document.id}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())

        chunks = ingest_pdf(file_path, user_id=current_user.id, document_id=document.id)

        document.chunks = chunks
        db.commit()

    return {
        "status": "success",
        "filename": file.filename,
        "document_id": document.id,
        "chunks": chunks,
    }


@app.post("/ask")
def ask(request: QuestionRequest, current_user: User = Depends(get_current_user)):
    return run_agent(
        request.question,
        user_id=current_user.id,
        intent="qa",
        document_ids=request.document_ids,
    )


@app.post("/summary")
def summary(request: QuestionRequest = QuestionRequest(question=""), current_user: User = Depends(get_current_user)):
    return run_agent(
        "Summarize the document",
        user_id=current_user.id,
        intent="summary",
        document_ids=request.document_ids,
    )


@app.post("/quiz")
def quiz(request: QuestionRequest = QuestionRequest(question=""), current_user: User = Depends(get_current_user)):
    return run_agent(
        "Generate a quiz",
        user_id=current_user.id,
        intent="quiz",
        document_ids=request.document_ids,
    )


@app.post("/topics")
def topics(request: QuestionRequest = QuestionRequest(question=""), current_user: User = Depends(get_current_user)):
    return run_agent(
        "Extract topics",
        user_id=current_user.id,
        intent="topics",
        document_ids=request.document_ids,
    )


@app.post("/explain")
def explain(request: QuestionRequest = QuestionRequest(question=""), current_user: User = Depends(get_current_user)):
    return run_agent(
        "Explain simply",
        user_id=current_user.id,
        intent="explain",
        document_ids=request.document_ids,
    )


@app.post("/agent")
def agent(request: QuestionRequest, current_user: User = Depends(get_current_user)):
    return run_agent(
        request.question,
        user_id=current_user.id,
        document_ids=request.document_ids,
    )


@app.delete("/documents/{document_id}")
def delete_document_route(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_document(user_id=current_user.id, document_id=document_id)
    db.delete(doc)
    db.commit()
    return {"status": "deleted"}


@app.get("/stats")
def get_stats(current_user: User = Depends(get_current_user)):
    try:
        with httpx.Client(auth=(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY), timeout=10) as client:
            questions_resp = client.get(
                f"{LANGFUSE_HOST}/api/public/traces",
                params={"name": "edurag-agent-run", "userId": current_user.id, "limit": 50},
            )
            questions_resp.raise_for_status()
            questions_data = questions_resp.json()

            uploads_resp = client.get(
                f"{LANGFUSE_HOST}/api/public/traces",
                params={"name": "pdf-upload", "userId": current_user.id, "limit": 1},
            )
            uploads_resp.raise_for_status()
            uploads_data = uploads_resp.json()

        traces = questions_data.get("data", [])
        total_questions = questions_data.get("meta", {}).get("totalItems", len(traces))
        total_uploads = uploads_data.get("meta", {}).get("totalItems", 0)

        latencies = [t["latency"] for t in traces if t.get("latency") is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0

        all_scores = []
        for t in traces:
            for s in t.get("scores", []):
                if isinstance(s, dict) and "value" in s:
                    all_scores.append(s["value"])
        avg_eval_score = (sum(all_scores) / len(all_scores) * 100) if all_scores else None

        stats = [
            {"label": "Your Questions Asked", "value": str(total_questions)},
            {"label": "Your Avg Response Time", "value": f"{avg_latency:.1f}", "unit": "s"},
            {"label": "Your PDFs Uploaded", "value": str(total_uploads)},
        ]

        if avg_eval_score is not None:
            stats.append({"label": "Eval Pass Rate", "value": f"{avg_eval_score:.0f}", "unit": "%"})

        return {"stats": stats}

    except Exception as e:
        return {"stats": None, "error": str(e)}


@app.get("/documents")
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    return {
        "documents": [
            {
                "id": d.id,
                "filename": d.filename,
                "chunks": d.chunks,
                "uploaded_at": d.uploaded_at.isoformat(),
            }
            for d in documents
        ]
    }