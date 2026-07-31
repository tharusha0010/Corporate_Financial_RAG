# 📚 OmniDoc-RAG

### Advanced Universal Document Analysis & RAG System

> **Scope:** Enterprise-grade intelligent retrieval and synthesis of information from diverse PDF documents.

OmniDoc-RAG is a full-stack, production-grade Retrieval-Augmented Generation (RAG) system designed to accurately answer complex queries based on any uploaded PDF documents. The system uses a **Hybrid Search Pipeline**, a **Cross-Encoder Reranker**, and a locally hosted LLM via OLLAMA to ensure high-precision data retrieval and complete data privacy. 

---

## ✨ Features

- **Universal Document Processing** — Simultaneously upload and process one or more PDF documents (e.g., Research Papers, Lecture Notes, Contracts) directly through the user interface.
- **Hybrid Search Retrieval** — Combines Semantic Vector Search (ChromaDB + HuggingFace Embeddings) with Keyword Search (BM25) for absolute precision.
- **Cross-Encoder Reranking** — Uses `ms-marco-MiniLM-L-6-v2` to intelligently rerank and filter the most relevant context chunks.
- **Local LLM Integration** — Powered by state-of-the-art open-source models via OLLAMA for generating accurate answers with zero API costs and 100% privacy.
- **Scientific Evaluation** — Built-in RAGAS framework script to measure model Faithfulness and Answer Relevancy.
- **Full-Stack Architecture** — Robust backend powered by **FastAPI** paired with an interactive **Streamlit** UI.
- **Source Citations** — Dynamically displays referenced document names, page numbers, and text snippets for maximum transparency.

---

## 📁 Project Structure

```text
OmniDoc-RAG/
├── app.py                              # Streamlit UI (Frontend)
├── api.py                              # FastAPI Backend (RAG Pipeline)
├── evaluate.py                         # RAGAS Evaluation Script
├── data/                               # Directory for uploaded documents
├── requirements.txt                    # Python dependencies
└── README.md                           # This file

```

---

## 🛠️ Prerequisites

| Requirement | Details |
| --- | --- |
| **Python** | 3.8 or higher |
| **OLLAMA** | Installed and running ([ollama.com](https://ollama.com)) |
| **Model** | `llama3` or `gemma3:12b` (Configurable based on hardware) |
| **Hardware** | PC/Laptop capable of running local LLMs (GPU recommended) |

---

## 🚀 Setup & Installation

### 1. Clone the project

```bash
git clone [https://github.com/tharusha0010/OmniDoc-RAG.git](https://github.com/tharusha0010/OmniDoc-RAG.git)
cd OmniDoc-RAG

```

### 2. Create a virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Linux/Mac

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Install and start OLLAMA

Download from [ollama.com](https://ollama.com), then run your preferred model:

```bash
ollama run llama3

```

---

## 📖 How to Use

1. **Start the API Backend:** Open a terminal, activate the virtual environment, and run:

```bash
uvicorn api:app --reload

```

2. **Start the Streamlit UI:** Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run app.py

```

3. The app will open at `http://localhost:8501`.
4. **Upload PDFs:** Use the sidebar to upload one or more PDF documents, then click **"Process PDFs"**.
5. **Ask a question** in the chat interface.
6. Review the synthesized answer and view the retrieved **Sources** (Document Name, Page Number, and Snippets) to verify the data against the original PDFs.

---

## 🏗️ Architecture

```text
User Question (Streamlit UI)
        │
        ▼
┌───────────────────────────────────┐
│        Hybrid Retrieval           │
│  ChromaDB (Vector) + BM25 (Text)  │
│  → Retrieves Top 5 + Top 5 Chunks │
└─────────────────┬─────────────────┘
                  ▼
┌───────────────────────────────────┐
│          Deduplication            │
│  → Filters Unique Document Chunks │
└─────────────────┬─────────────────┘
                  ▼
┌───────────────────────────────────┐
│      Cross-Encoder Reranker       │
│  ms-marco-MiniLM-L-6-v2           │
│  → Selects Top 3 Most Relevant    │
└─────────────────┬─────────────────┘
                  ▼
┌───────────────────────────────────┐
│          Generation (LLM)         │
│  OLLAMA (Local LLM)               │
│  → Synthesizes Answer & Sources   │
└─────────────────┬─────────────────┘
                  ▼
         Streamlit Results UI

```

---

## 📦 Dependencies

| Package | Purpose |
| --- | --- |
| `fastapi` & `uvicorn` | Backend API framework and server |
| `streamlit` | Chatbot web UI framework |
| `langchain` ecosystem | RAG pipeline orchestration |
| `sentence-transformers` | Embeddings and Cross-Encoder reranking |
| `chromadb` | Vector database for semantic search |

---

## 📄 Author

This project was developed by **H.A.T.S. Ariyarathna** (Index: D/BCE/24/0010)

*3rd-year Computer Engineering Undergraduate | General Sir John Kotelawala Defence University (KDU)*

```




