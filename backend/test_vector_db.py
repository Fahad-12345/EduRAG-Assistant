# test_vector_db.py — run standalone
import os
from retrieval import retrieve_context
print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))
result = retrieve_context("What is throwaway prototyping?", apply_filter=False)
print(f"Docs found: {len(result['docs'])}")
print(result['context'][:200])