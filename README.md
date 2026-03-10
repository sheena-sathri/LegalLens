# LegalLens 🔍⚖️

**AI-Powered Legal Document Intelligence Platform**

LegalLens is an intelligent document analysis platform built for legal operations teams. It leverages LLMs, RAG (Retrieval-Augmented Generation), and document intelligence to automate contract review, document classification, clause extraction, and knowledge retrieval — enabling legal teams to work faster, smarter, and with greater consistency.

> Built as a proof-of-concept for AI-driven legal operations tooling. Demonstrates modern AI architecture patterns including context engineering, tool use, and retrieval-augmented generation.

---

## 🎯 Problem Statement

Legal departments at scale face critical challenges:

- **Volume**: Thousands of contracts, NDAs, and agreements flow through legal ops annually
- **Inconsistency**: Manual review leads to missed clauses, overlooked risks, and inconsistent analysis
- **Knowledge silos**: Institutional knowledge about contract patterns and precedents lives in people's heads
- **Slow turnaround**: Manual contract review creates bottlenecks that delay business deals

LegalLens addresses these by providing an AI-powered platform that augments legal professionals — not replacing their judgment, but amplifying their capacity.

---

## ✨ Features

### 1. Document Upload & Auto-Classification
Upload PDF, DOCX, or TXT legal documents with automatic classification into document types (NDA, MSA, SOW, Employment Agreement, Licensing Agreement, Amendment, etc.) with confidence scoring and batch upload support.

### 2. Intelligent Clause Extraction & Risk Flagging
Extracts key clauses (termination, liability/indemnification, IP assignment, confidentiality, non-compete, governing law, payment terms) with risk scoring per clause (Low / Medium / High / Critical). Highlights non-standard or potentially risky language with side-by-side comparison against standard clause templates.

### 3. RAG-Powered Q&A (Knowledge Retrieval)
Ask natural language questions about any uploaded document or across your entire document corpus. Citation-backed responses link back to source documents and specific passages. Supports cross-document queries like: *"Which of our vendor contracts have unlimited liability clauses?"*

### 4. Contract Comparison
Upload two versions of a contract to identify semantic differences — not just text diff, but meaning-level changes. Highlights new risks introduced in revised versions.

### 5. Knowledge Base & Playbook
Documents build a searchable vector knowledge base over time. Define your organization's contract playbook (preferred terms, fallback positions, red lines). AI references your playbook when analyzing new documents.

### 6. Governance & Audit Trail
Every query, analysis, and classification is logged. Track who reviewed what and when. Model confidence scores and data lineage for compliance. Export audit reports.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Upload   │ │ Analysis │ │ Q&A Chat │ │ Knowledge  │ │
│  │ Portal   │ │ Dashboard│ │ Interface│ │ Base Mgmt  │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              API Router Layer                      │   │
│  │  /upload  /classify  /extract  /ask  /compare     │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │            Core Services                          │   │
│  │  Document Processor  │  Classification Engine     │   │
│  │  Clause Extractor    │  RAG Engine                │   │
│  │  Comparator Service  │  Governance Logger         │   │
│  └──────────────────────────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │          LLM Orchestration Layer                   │   │
│  │  Context Engineer  │  Tool Use Manager            │   │
│  │  Prompt Templates  │  Response Parser             │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  ChromaDB    │ │  SQLite      │ │  Claude API  │
│  (Vectors)   │ │  (Metadata)  │ │  (LLM)       │
│ - Embeddings │ │ - Documents  │ │ - Analysis   │
│ - Chunks     │ │ - Audit logs │ │ - Extraction │
│ - Retrieval  │ │ - Users      │ │ - Q&A        │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Streamlit | Rapid prototyping, clean UI, built-in file upload |
| Backend API | FastAPI | Async, type-safe, auto-docs, Python-native |
| LLM | Claude API (Anthropic) | Strong reasoning, long context window, tool use |
| Vector DB | ChromaDB | Lightweight, embedded, perfect for prototyping |
| Metadata DB | SQLite | Zero-config, sufficient for POC |
| Doc Parsing | PyMuPDF + python-docx | Robust PDF/DOCX text extraction |
| Embeddings | sentence-transformers | Local embeddings, no API dependency |

---

## 📁 Project Structure

```
legallens/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                          # FastAPI app entry point
├── config.py                        # Configuration & env vars
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py         # Upload, list, delete
│   │       ├── analysis.py          # Classification, extraction
│   │       ├── search.py            # RAG Q&A endpoints
│   │       └── governance.py        # Audit trail, export
│   ├── core/
│   │   ├── document_processor.py    # Parse PDF/DOCX → text
│   │   ├── classifier.py            # Document type classification
│   │   ├── clause_extractor.py      # Extract & score clauses
│   │   ├── rag_engine.py            # RAG pipeline
│   │   ├── comparator.py            # Contract comparison
│   │   └── governance.py            # Audit logging
│   ├── llm/
│   │   ├── client.py                # Claude API wrapper
│   │   ├── prompts.py               # Prompt templates
│   │   ├── context_engineer.py      # Context window mgmt
│   │   └── tools.py                 # Tool definitions
│   ├── db/
│   │   ├── vector_store.py          # ChromaDB operations
│   │   ├── metadata_store.py        # SQLite operations
│   │   └── models.py                # Pydantic data models
│   └── utils/
│       ├── chunking.py              # Text chunking strategies
│       └── text_processing.py       # Text cleaning
├── frontend/
│   └── streamlit_app.py             # Streamlit UI
├── data/
│   ├── sample_contracts/            # Sample legal docs for demo
│   └── playbooks/
│       └── default_playbook.json    # Default review playbook
└── tests/
    ├── test_classifier.py
    ├── test_extractor.py
    └── test_rag.py
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/legallens.git
cd legallens
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run backend
uvicorn main:app --reload --port 8000

# Run frontend (separate terminal)
streamlit run frontend/streamlit_app.py
```

---

## 🔑 Key Design Decisions

### Why RAG over Fine-tuning?
Legal documents are organization-specific — fine-tuning would require proprietary training data. RAG allows the system to work with any organization's documents immediately, is easier to maintain and audit, and retrieval sources are traceable (critical for legal compliance).

### Why Claude API?
Superior reasoning for complex legal language, 200K context window handles long contracts, native tool use for structured extraction, and strong instruction following for consistent output.

### Context Engineering Approach
Dynamic context assembly gives each query a custom context window with relevant document chunks, playbook rules, and task-specific instructions. Legal documents are chunked by section/clause boundaries (not arbitrary token counts), and retrieval combines semantic similarity with metadata filters.

### Governance by Design
Every LLM call is logged with input hash, output, latency, and confidence. Document access is tracked. No document content is stored in the LLM.

---

## 🗺️ Roadmap

- [ ] v0.1 — Core document upload, classification, clause extraction
- [ ] v0.2 — RAG-powered Q&A with citation support
- [ ] v0.3 — Contract comparison and playbook integration
- [ ] v0.4 — Governance dashboard and audit export
- [ ] v1.0 — Multi-user support, RBAC, SSO integration

---

## 📄 License

MIT License

## 👤 Author

**Sheena** — Architected Data Science and Engineering Systems across Microsoft, Apple, and Meta.
