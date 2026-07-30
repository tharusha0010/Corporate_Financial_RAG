

```markdown
# 📈 Corporate Financial RAG System

### Advanced Financial Document Analysis — AI & Machine Learning Engineering

> **Scope:** Enterprise-grade intelligent retrieval and synthesis of corporate financial data (e.g., Annual 10-K reports)

A full-stack, production-grade Retrieval-Augmented Generation (RAG) system designed to accurately answer complex queries based on corporate financial documents. The system uses a **Hybrid Search Pipeline**, a **Cross-Encoder Reranker**, and a locally hosted LLM via OLLAMA to ensure high-precision data retrieval and complete data privacy. It also includes scientific evaluation using the **RAGAS framework**.

---

## ✨ Features

- **Hybrid Search Retrieval** — Combines Semantic Vector Search (ChromaDB + HuggingFace Embeddings) with Keyword Search (BM25) for absolute precision.
- **Cross-Encoder Reranking** — Uses `ms-marco-MiniLM-L-6-v2` to intelligently rerank and filter the most relevant context chunks.
- **Local LLM Integration** — Powered by **Gemma 3 (12B)** via OLLAMA for generating accurate financial answers with zero API costs.
- **Scientific Evaluation** — Built-in RAGAS framework script to measure model Faithfulness and Answer Relevancy.
- **Full-Stack Architecture** — Robust backend powered by **FastAPI** paired with a **Streamlit** UI.
- **Source Citations** — Dynamically displays referenced page numbers and document snippets for transparency.

---

## 📁 Project Structure

```text
Corporate_Financial_RAG/
├── app.py                              # Streamlit UI (Frontend)
├── api.py                              # FastAPI Backend (RAG Pipeline)
├── evaluate.py                         # RAGAS Evaluation Script
├── data/
│   └── report.pdf                      # Financial document (e.g., Tesla 10-K)
├── requirements.txt                    # Python dependencies
└── README.md                           # This file

```

---

## 🛠️ Prerequisites

| Requirement | Details |
| --- | --- |
| **Python** | 3.8 or higher |
| **OLLAMA** | Installed and running ([ollama.com](https://ollama.com)) |
| **Model** | `gemma3:12b` |
| **Hardware** | PC/Laptop capable of running local 12B parameter LLMs |
| **Data** | A valid PDF financial report placed inside the `data/` directory |

---

## 🚀 Setup & Installation

### 1. Clone the project

```bash
git clone [https://github.com/tharusha0010/Corporate_Financial_RAG.git](https://github.com/tharusha0010/Corporate_Financial_RAG.git)
cd Corporate_Financial_RAG

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

Download from [ollama.com](https://ollama.com), then:

```bash
ollama run gemma3:12b

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
4. **Ask a question** (e.g., *"What is the total revenue for 2023?"*) in the chat interface.
5. Review the synthesized answer and click **"📚 View Retrieved Sources"** to verify the data against the original PDF.
6. **(Optional)** Run `python evaluate.py` to test the system's accuracy using RAGAS.

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
│         Generation (LLM)          │
│  OLLAMA (gemma3:12b)              │
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
| `ragas` | Evaluation metrics (Faithfulness & Relevancy) |

---

## 📄 Author

This project was developed by **H.A.T.S. Ariyarathna** 

*General Sir John Kotelawala Defence University (KDU)*

```
