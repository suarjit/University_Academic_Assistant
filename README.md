# University Academic Information Assistant (RAG)

## Project Overview

The University Academic Information Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer student queries using university documents.

The system retrieves relevant information from university documents and uses Google's Gemini model to generate concise, context-based answers with source citations.

It also supports abstention when the available documents do not contain sufficient information to answer a question.

**Important:** Greenfield University and all university documents included in this project are fictional sample data created for development and testing purposes. They do not represent a real university or official academic policies.

## Key Features

- Document ingestion from TXT, PDF, and HTML files.
- Text cleaning and preprocessing.
- Document chunking with overlap.
- Semantic search using sentence-transformer embeddings.
- Persistent vector storage using ChromaDB.
- Context-based answer generation using Gemini.
- Source citations in generated answers.
- Abstention when sufficient evidence is unavailable.
- Streamlit-based interactive interface.
- Automated evaluation using 15 test questions.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| LLM | Google Gemini |
| Embedding Model | all-MiniLM-L6-v2 |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| Document Processing | PyPDF, BeautifulSoup |
| Evaluation | Python |
| Version Control | Git |

## Project Architecture

```text
University_Academic_Assistant/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── evaluation/
│   ├── evaluation_dataset.json
│   ├── evaluation_results.json
│   └── run_evaluation.py
│
├── src/
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   └── text_processor.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   └── answer_generator.py
│   │
│   ├── vectorstore/
│   │   └── vector_store.py
│   │
│   └── indexing/
│       └── index_documents.py
│
├── tests/
├── vectorstore/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd University_Academic_Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your actual API key to GitHub.

## Running the Project

### Step 1: Index university documents

```bash
python src/indexing/index_documents.py
```

This loads the documents, processes their text, generates embeddings, and stores them in ChromaDB.

### Step 2: Launch the application

```bash
streamlit run app/streamlit_app.py
```

Open the local URL displayed in your terminal to interact with the application.

## RAG Pipeline

1. **Document Ingestion:** Loads university documents in TXT, PDF, and HTML formats.
2. **Preprocessing:** Cleans extracted text and removes unnecessary whitespace.
3. **Chunking:** Splits documents into smaller overlapping text chunks.
4. **Embedding Generation:** Converts text chunks into numerical vector representations.
5. **Vector Storage:** Stores embeddings and metadata in ChromaDB.
6. **Retrieval:** Retrieves relevant document chunks using semantic similarity search.
7. **Answer Generation:** Sends the retrieved context and student question to Gemini.
8. **Citation and Abstention:** Generates source-attributed answers or abstains when evidence is insufficient.

## Evaluation

The system was evaluated using 15 test questions:

- 10 answerable questions.
- 5 questions requiring abstention.

### Final Evaluation Results

| Evaluation Metric | Result |
|---|---:|
| Retrieval Source Accuracy | 100% (10/10) |
| Evidence Support Accuracy | 100% (10/10) |
| Citation Support Accuracy | 100% (10/10) |
| Abstention Accuracy | 100% (5/5) |
| Answer Generation Success | 100% (10/10) |

Detailed evaluation results are available in:

`evaluation/evaluation_results.json`

**Evaluation note:** These results represent the project's current 15-question test set. They should not be interpreted as a guarantee of 100% accuracy on unseen questions. Evidence support is assessed using a lexical overlap heuristic, not an independent human factual-verification process.

## Limitations

- Answer quality depends on the quality and completeness of the supplied documents.
- The evaluation dataset is relatively small.
- Evidence support evaluation uses lexical matching and may not detect every factual error.
- Gemini API access and internet connectivity are required for answer generation.
- The included university documents are fictional sample data.

## Future Improvements

- Add support for DOCX documents.
- Expand the evaluation dataset.
- Implement more robust factual citation verification.
- Improve retrieval using reranking.
- Add conversation memory and document management.
- Deploy the application to a cloud platform.

## Author

**Surajit Bera**

## Project Purpose

Developed as part of a Data Science / Generative AI internship project to demonstrate document ingestion, RAG indexing and retrieval, LLM-based answer generation, citation handling, abstention, and evaluation.