import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# VECTOR_DB = os.path.join(BASE_DIR, "vector_db")

DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB = os.path.join(DATA_DIR, "vector_db")


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def get_collection_name(user_id: str) -> str:
    return f"user_{user_id}"


# def reset_vector_db(user_id: str):
#     embeddings = get_embeddings()

#     db = Chroma(
#         collection_name=get_collection_name(user_id),
#         persist_directory=VECTOR_DB,
#         embedding_function=embeddings,
#     )

#     existing = db.get()

#     if existing and existing.get("ids"):
#         db.delete(ids=existing["ids"])


def ingest_pdf(file_path: str, user_id: str, document_id: str):
    """Adds a document's chunks to the user's collection, tagged with document_id.
    Does NOT wipe existing documents — multiple uploads now coexist."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["document_id"] = document_id

    embeddings = get_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB,
        collection_name=get_collection_name(user_id),
    )

    return len(chunks)


def delete_document(user_id: str, document_id: str):
    """Removes all chunks belonging to a specific document from the user's collection."""
    embeddings = get_embeddings()
    db = Chroma(
        collection_name=get_collection_name(user_id),
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )
    db.delete(where={"document_id": document_id})