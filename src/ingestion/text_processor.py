
import re
from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """
    Clean extracted document text by removing
    unnecessary spaces and formatting issues.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text


def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[str]:
    """
    Split text into smaller overlapping chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len
    )

    chunks = splitter.split_text(text)

    return chunks


def process_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Dict]:
    """
    Clean documents and split them into chunks.
    Preserve source metadata for later citations.
    """

    processed_chunks = []

    for document in documents:

        cleaned_text = clean_text(document["text"])

        chunks = split_text_into_chunks(
            cleaned_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk_index, chunk in enumerate(chunks):

            processed_chunks.append({
                "text": chunk,
                "source": document["source"],
                "file_type": document["file_type"],
                "chunk_id": chunk_index
            })

    return processed_chunks
