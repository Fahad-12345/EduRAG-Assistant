# reindex_test_data.py
from rag import ingest_pdf

for user_id in ["mcp-client", "eval-script"]:
    chunks = ingest_pdf("uploads/Software Prototyping Techniques.pdf", user_id=user_id)
    print(f"Indexed {chunks} chunks for {user_id}")