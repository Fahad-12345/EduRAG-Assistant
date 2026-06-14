import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

VECTOR_DB = "vector_db"
COLLECTION_NAME = "current_document"


def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")


def reset_vector_db():
    embeddings = get_embeddings()

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )

    existing = db.get()

    if existing and existing.get("ids"):
        db.delete(ids=existing["ids"])


def ingest_pdf(file_path):
    reset_vector_db()

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB,
        collection_name=COLLECTION_NAME,
    )

    return len(chunks)


def ask_question(question):
    embeddings = get_embeddings()

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )

    docs = db.similarity_search(question, k=4)

    context = ""

    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")

        context += f"""
Source {i + 1}:
File: {source}
Page: {page + 1 if isinstance(page, int) else page}

Content:
{doc.page_content}
"""

    llm = ChatOllama(model="gemma2:2b")

    prompt = f"""
You are an AI University Assistant.

Answer the student's question using only the context below.
If the answer is not available in the context, say:
"I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer_text = response.content.strip()

    not_found_phrases = [
    "I could not find this information in the uploaded document",
    "could not find this information",
    "not available in the context",
    "not available in the uploaded document",
    ]
    if any(phrase.lower() in answer_text.lower() for phrase in not_found_phrases):
     return {
        "answer": answer_text,
        "sources": []
      }
    sources = []

    for doc in docs:
     source = doc.metadata.get("source", "Unknown file")
     page = doc.metadata.get("page", "Unknown page")

     source_item = {
        "file": os.path.basename(source),
        "page": page + 1 if isinstance(page, int) else page
     }

     if source_item not in sources:
        sources.append(source_item)

    return {
    "answer": answer_text,
    "sources": sources
  }


def generate_summary():
    return ask_question(
        "Summarize this uploaded document in clear bullet points. Keep it useful for a university student."
    )
def generate_quiz():
    return ask_question(
        """
Generate 10 quiz questions from the uploaded document.

Format:
1. Question
A) Option A
B) Option B
C) Option C
D) Option D
Answer: Correct option

Keep the questions clear and useful for university students.
"""
    )
def generate_topics():
    return ask_question(
        """
Extract the main key topics covered in the uploaded document.

Format the answer as:
- Topic 1
- Topic 2
- Topic 3

Only include important academic or technical topics.
"""
    )
def explain_simply():
    return ask_question(
        """
Explain the uploaded document in simple and easy-to-understand language.

Assume the reader is a university student who is seeing this topic for the first time.

Use simple words and short paragraphs.
"""
    )