
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from vectorstore.vector_store import (
    load_vector_store,
    search_similar_documents
)


def retrieve_documents(query: str, k: int = 4):
    """Retrieve relevant university document chunks."""

    vector_store = load_vector_store()

    results = search_similar_documents(
        vector_store=vector_store,
        query=query,
        k=k
    )

    retrieved_documents = []

    for document, score in results:
        retrieved_documents.append({
            "text": document.page_content,
            "source": document.metadata["source"],
            "chunk_id": document.metadata["chunk_id"],
            "score": float(score)
        })

    return retrieved_documents
