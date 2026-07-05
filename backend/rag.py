import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

VECTOR_DB = "vector_db"
COLLECTION_NAME = "current_document"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


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
