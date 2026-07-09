# retrieval.py
import os
from rag import get_embeddings, VECTOR_DB, get_collection_name
from langchain_chroma import Chroma
from langfuse import get_client


def retrieve_context(question, user_id: str, k=4, max_distance=1.4, apply_filter=True):
    embeddings = get_embeddings()
    db = Chroma(
        collection_name=get_collection_name(user_id),
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )

    results = db.similarity_search_with_score(question, k=k)

    get_client().update_current_span(
        metadata={"retrieval_distances": [round(d, 3) for _, d in results]}
    )

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