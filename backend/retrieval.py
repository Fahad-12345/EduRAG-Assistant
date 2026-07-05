# retrieval.py
import os
from rag import get_embeddings, VECTOR_DB, COLLECTION_NAME
from langchain_chroma import Chroma

def retrieve_context(question, k=4, max_distance=1.4, apply_filter=True):
    embeddings = get_embeddings()
    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )

    results = db.similarity_search_with_score(question, k=k)

    if apply_filter:
        results = [(doc, d) for doc, d in results if d <= max_distance]

    docs = [doc for doc, d in results]

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
    return {"docs": docs, "context": context}