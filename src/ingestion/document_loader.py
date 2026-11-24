
from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from bs4 import BeautifulSoup


def load_txt(file_path: Path) -> str:
    """Read text from a TXT file."""
    return file_path.read_text(encoding="utf-8")


def load_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(str(file_path))

    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


def load_html(file_path: Path) -> str:
    """Extract readable text from an HTML file."""
    html_content = file_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html_content, "lxml")

    # Remove unnecessary elements
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    return soup.get_text(separator="\n", strip=True)


def load_document(file_path: Path) -> Dict:
    """Load a document based on its file extension."""

    extension = file_path.suffix.lower()

    if extension == ".txt":
        text = load_txt(file_path)

    elif extension == ".pdf":
        text = load_pdf(file_path)

    elif extension in [".html", ".htm"]:
        text = load_html(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return {
        "source": file_path.name,
        "file_path": str(file_path),
        "file_type": extension,
        "text": text
    }


def load_documents(data_directory: Path) -> List[Dict]:
    """Load all supported documents from a directory."""

    documents = []

    supported_extensions = {
        ".txt",
        ".pdf",
        ".html",
        ".htm"
    }

    for file_path in data_directory.iterdir():

        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:

            document = load_document(file_path)

            if document["text"].strip():
                documents.append(document)

    return documents
