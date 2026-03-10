# LegalLens: Technical Design Document
## AI-Powered Legal Document Intelligence Platform

**Author:** Sheena  
**Date:** February 2026  
**Version:** 0.1  

---

## Executive Summary

LegalLens is a prototype AI platform designed for legal operations teams to automate document classification, clause extraction, risk assessment, and knowledge retrieval across legal document portfolios. It demonstrates how modern AI architecture patterns — including retrieval-augmented generation (RAG), context engineering, and LLM tool use — can transform legal workflows while maintaining governance and auditability.

This document outlines the system design, architecture decisions, and implementation approach.

---

## 1. Problem & Opportunity

Legal departments at enterprise scale face compounding challenges:

**Volume & Velocity:** A legal ops team at a company like Apple may process thousands of contracts, NDAs, vendor agreements, and amendments annually. Manual review creates bottlenecks.

**Inconsistency:** Different reviewers apply different standards. Critical clauses get missed. Risk assessments vary by who happens to review the document.

**Knowledge Fragmentation:** Institutional knowledge about preferred contract terms, past negotiation outcomes, and risk patterns lives in individual attorneys' heads rather than in searchable, reusable systems.

**Compliance Burden:** Regulatory requirements (GDPR, CCPA, EU AI Act) demand auditable processes for how legal decisions are made and documented.

LegalLens addresses these by providing an AI layer that augments legal professionals — ensuring consistency, surfacing risks proactively, and making the organization's collective legal knowledge searchable.

---

## 2. Architecture Overview

### 2.1 System Design

LegalLens follows a three-tier architecture:

```
[Streamlit UI] → [FastAPI Backend] → [LLM + Vector DB + SQLite]
```

**Frontend (Streamlit):** Rapid-prototype UI with document upload, analysis dashboards, chat-based Q&A, and governance views. Chosen for speed-to-demo; production would use React.

**Backend (FastAPI):** Async Python API handling document processing, LLM orchestration, and data management. FastAPI provides automatic OpenAPI docs, type safety via Pydantic, and async support for concurrent LLM calls.

**Data Layer:**
- **ChromaDB** (Vector Store): Stores document chunk embeddings for semantic search
- **SQLite** (Metadata Store): Stores document metadata, classifications, audit logs
- **Claude API** (LLM): Powers classification, extraction, Q&A, and comparison

### 2.2 Data Flow

```
Upload → Parse (PyMuPDF/python-docx) → Clean → Chunk (section-aware)
  ↓
  ├→ Embed & Index (ChromaDB)
  ├→ Store metadata (SQLite)
  └→ Classify (Claude) → Extract clauses (Claude) → Risk score
  
Query → Retrieve chunks (ChromaDB) → Assemble context → Generate (Claude) → Cite sources
```

---

## 3. Core Components

### 3.1 Document Processor

Handles PDF and DOCX ingestion with format-specific extraction:
- **PDF:** PyMuPDF for text extraction with layout awareness
- **DOCX:** python-docx for paragraph and table extraction
- **Cleaning:** Removes headers/footers, page numbers, normalizes whitespace
- **Section Detection:** Regex-based detection of legal section patterns (ARTICLE I, Section 1.2, etc.)

### 3.2 Section-Aware Chunking

Legal documents have meaningful structure that naive token-based chunking destroys. LegalLens chunks by:

1. **Section boundaries first** — respecting ARTICLE/SECTION/clause markers
2. **Paragraph boundaries** — if a section exceeds the chunk size limit
3. **Sentence boundaries** — as a last-resort fallback

This ensures that a "Limitation of Liability" clause is never split across two chunks, preserving semantic integrity during retrieval.

### 3.3 Classification Engine

Uses Claude with a structured system prompt to classify documents into legal categories (NDA, MSA, SOW, etc.) with:
- Primary and secondary classifications with confidence scores
- Automated metadata extraction (parties, dates, governing law)
- Context engineering to prioritize document beginning (where type is declared) and end (signatures, governing terms)

### 3.4 Clause Extraction & Risk Assessment

The extraction pipeline:
1. Sends the full document to Claude with a detailed system prompt defining clause types and risk levels
2. Includes the organization's **contract playbook** in the context — preferred terms, fallback positions, and red lines
3. Claude identifies each clause, extracts the relevant text, assigns a risk level, and provides actionable playbook-aligned recommendations
4. Results are stored for future reference and cross-document analysis

Risk levels are calibrated:
- **LOW:** Standard, market-friendly terms
- **MEDIUM:** Slightly non-standard but acceptable
- **HIGH:** Significantly deviates from market standard
- **CRITICAL:** Could expose the organization to material risk

### 3.5 RAG Engine

The retrieval-augmented generation pipeline for document Q&A:

1. **Retrieve:** Query ChromaDB for semantically similar chunks (cosine similarity)
2. **Filter:** Optionally scope to specific documents
3. **Assemble:** Build a context window with retrieved chunks, respecting token budget
4. **Generate:** Claude answers the question based only on provided context
5. **Cite:** Every claim is linked back to source document and section

Key design choice: RAG over fine-tuning because:
- Legal documents are organization-specific and proprietary
- Retrieval sources are traceable (critical for legal compliance)
- No training data leakage risk
- System works immediately with any organization's documents

### 3.6 Contract Comparison

Semantic comparison (not just text diff):
- Identifies changes in legal meaning, rights, and obligations
- Categorizes changes as added/removed/modified
- Assesses risk impact of each change
- Flags new risks introduced in revised versions

### 3.7 Governance & Audit Trail

Every LLM interaction is logged:
- Timestamp, action type, document ID
- Input summary (hashed for privacy)
- Output summary, model used, latency
- Confidence scores

This supports compliance requirements and provides transparency into AI-assisted decisions.

---

## 4. Context Engineering

Context engineering is central to LegalLens's effectiveness. Rather than sending raw text to the LLM, each task gets a purpose-built context window:

### 4.1 Dynamic Context Assembly

Each task type has its own context strategy:

| Task | Strategy |
|------|----------|
| Classification | 60% doc beginning + 40% doc end (type declared at start, terms at end) |
| Extraction | Full doc + playbook injected as reference |
| Q&A | Retrieved chunks ranked by relevance, budget-fitted |
| Comparison | Both versions side-by-side, proportionally truncated |

### 4.2 Token Budget Management

With Claude's 200K context window, most legal documents fit without truncation. For very long documents:
- Estimate token count using tiktoken
- Reserve budget for system prompt (~2K) and output (~4K)
- Allocate remaining budget to document content
- Truncate strategically (not arbitrarily) based on task type

### 4.3 Prompt Engineering

Each task uses a specialized system prompt that:
- Defines Claude's role and expertise
- Specifies exact output format (JSON schema)
- Includes guardrails against hallucination
- Provides few-shot examples where needed

---

## 5. Tool Use Architecture

LegalLens defines tools that Claude can invoke during complex queries:

- `search_knowledge_base` — retrieve relevant chunks across documents
- `get_document_metadata` — look up document classification and details
- `get_clause_details` — retrieve extraction results for a document
- `check_playbook` — consult the organization's contract playbook

This enables multi-step reasoning: "Compare the liability terms in our current MSA with what our playbook recommends" requires Claude to fetch the MSA's extracted clauses, then check the playbook, then synthesize.

---

## 6. Production Considerations

While LegalLens is a prototype, the architecture is designed with production readiness in mind:

### 6.1 What Would Change for Production

| Prototype | Production |
|-----------|------------|
| Streamlit UI | React + TypeScript frontend |
| SQLite | PostgreSQL with proper migrations |
| ChromaDB | Pinecone or Weaviate (managed, scalable) |
| Single-user | Multi-tenant with RBAC and SSO |
| Local embeddings | Dedicated embedding service |
| Synchronous LLM calls | Async with queue (Celery/SQS) |

### 6.2 Security & Privacy

- Document content never stored in LLM training data (API usage)
- All documents encrypted at rest
- Role-based access control for document visibility
- Audit trail for compliance and forensics
- PII detection and redaction before LLM processing

### 6.3 Integration Points

Designed to integrate with enterprise legal tools:
- **DMS:** iManage, NetDocuments (document ingestion)
- **CLM:** Ironclad, Icertis (contract lifecycle)
- **eDiscovery:** Relativity, Nuix (document review)
- **SSO:** Okta, Azure AD (authentication)

---

## 7. Tech Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Backend | FastAPI (Python) | Async, type-safe, auto-docs |
| Frontend | Streamlit | Rapid prototyping |
| LLM | Claude API | Superior reasoning, 200K context, tool use |
| Vector DB | ChromaDB | Lightweight, embedded, cosine similarity |
| Metadata DB | SQLite | Zero-config, sufficient for POC |
| Doc Parsing | PyMuPDF + python-docx | Robust extraction |
| Embeddings | sentence-transformers | Local, no API dependency |

---

## 8. Roadmap

- **v0.1** — Document upload, classification, clause extraction *(current)*
- **v0.2** — RAG Q&A with citation support
- **v0.3** — Contract comparison, playbook integration
- **v0.4** — Governance dashboard, audit export
- **v1.0** — Multi-user, RBAC, SSO, CLM/DMS integrations

---

## 9. Why This Matters for Legal Ops

Legal operations is at an inflection point. The combination of:
- LLMs capable of understanding legal language nuance
- RAG enabling organization-specific knowledge retrieval
- Structured tool use enabling multi-step legal reasoning
- Governance frameworks ensuring AI decisions are auditable

...creates an opportunity to fundamentally transform how legal departments operate — not by replacing attorneys, but by giving them AI-powered tools that ensure consistency, surface risks proactively, and make institutional knowledge accessible to every team member.

LegalLens is a proof of this concept.
