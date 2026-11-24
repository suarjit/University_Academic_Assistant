
import sys
from pathlib import Path

# Locate the project root and src directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from ingestion.document_loader import load_documents
from ingestion.text_processor import process_documents
from vectorstore.vector_store import create_vector_store


def main():
    """Load, process, embed, and index university documents."""

    data_directory = PROJECT_ROOT / "data" / "raw"

    print("=" * 60)
    print("UNIVERSITY DOCUMENT INDEXING PIPELINE")
    print("=" * 60)

    # Step 1: Load documents
    print("\n[1/4] Loading university documents...")

    documents = load_documents(data_directory)

    print(f"Documents loaded: {len(documents)}")

    if not documents:
        print("No supported documents found.")
        return

    # Step 2: Clean and split documents
    print("\n[2/4] Cleaning and splitting documents...")

    chunks = process_documents(
        documents,
        chunk_size=500,
        chunk_overlap=100
    )

    print(f"Total chunks generated: {len(chunks)}")

    # Step 3: Generate embeddings and store in ChromaDB
    print("\n[3/4] Generating embeddings and storing in ChromaDB...")
    print("The embedding model may download on its first run.")

    vector_store = create_vector_store(chunks)

    print("Embeddings generated and stored successfully.")

    # Step 4: Verify database
    print("\n[4/4] Verifying vector database...")

    collection_count = vector_store._collection.count()

    print(f"Vectors stored: {collection_count}")

    print("\n" + "=" * 60)
    print("DOCUMENT INDEXING COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
