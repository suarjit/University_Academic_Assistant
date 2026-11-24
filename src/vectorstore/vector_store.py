
from pathlib import Path
from typing import List, Dict

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Persistent database directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DB_PATH = PROJECT_ROOT / "vectorstore" / "chroma_db"

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def create_embedding_model():
    """
    Load the Hugging Face sentence-transformer embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def create_vector_store(
    chunks: List[Dict],
    embedding_model=None
) -> Chroma:
    """
    Convert document chunks into embeddings
    and store them persistently in ChromaDB.
    """

    if not chunks:
        raise ValueError("No document chunks provided.")

    if embedding_model is None:
        embedding_model = create_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "file_type": chunk["file_type"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=str(CHROMA_DB_PATH),
        collection_name="university_documents"
    )

    return vector_store


def load_vector_store(embedding_model=None) -> Chroma:
    """
    Load an existing persistent ChromaDB collection.
    """

    if not CHROMA_DB_PATH.exists():
        raise FileNotFoundError(
            f"Vector database not found: {CHROMA_DB_PATH}"
        )

    if embedding_model is None:
        embedding_model = create_embedding_model()

    vector_store = Chroma(
        collection_name="university_documents",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DB_PATH)
    )

    return vector_store


def search_similar_documents(
    vector_store: Chroma,
    query: str,
    k: int = 4
):
    """
    Retrieve the most relevant document chunks for a query.
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    return results
