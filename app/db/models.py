"""Data models for LegalLens."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# --- Enums ---

class DocumentType(str, Enum):
    NDA = "Non-Disclosure Agreement"
    MSA = "Master Service Agreement"
    SOW = "Statement of Work"
    EMPLOYMENT = "Employment Agreement"
    LICENSE = "Licensing Agreement"
    AMENDMENT = "Amendment"
    LEASE = "Lease Agreement"
    PURCHASE = "Purchase Agreement"
    PARTNERSHIP = "Partnership Agreement"
    TERMS_OF_SERVICE = "Terms of Service"
    PRIVACY_POLICY = "Privacy Policy"
    OTHER = "Other"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ClauseType(str, Enum):
    TERMINATION = "Termination"
    LIABILITY = "Limitation of Liability"
    INDEMNIFICATION = "Indemnification"
    CONFIDENTIALITY = "Confidentiality"
    IP_ASSIGNMENT = "IP Assignment"
    NON_COMPETE = "Non-Compete"
    NON_SOLICITATION = "Non-Solicitation"
    GOVERNING_LAW = "Governing Law"
    DISPUTE_RESOLUTION = "Dispute Resolution"
    PAYMENT_TERMS = "Payment Terms"
    DATA_PROTECTION = "Data Protection"
    FORCE_MAJEURE = "Force Majeure"
    ASSIGNMENT = "Assignment"
    INSURANCE = "Insurance"
    WARRANTIES = "Warranties"
    OTHER = "Other"


# --- Request Models ---

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    page_count: int
    character_count: int
    status: str = "uploaded"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ClassificationResult(BaseModel):
    document_id: str
    document_type: DocumentType
    confidence: float = Field(ge=0.0, le=1.0)
    secondary_type: Optional[DocumentType] = None
    secondary_confidence: Optional[float] = None
    reasoning: str = ""


class ExtractedClause(BaseModel):
    clause_type: ClauseType
    text: str
    section_reference: str = ""
    risk_level: RiskLevel
    risk_reason: str = ""
    playbook_note: str = ""


class ExtractionResult(BaseModel):
    document_id: str
    clauses: list[ExtractedClause]
    metadata: dict = {}
    summary: str = ""


class DocumentMetadata(BaseModel):
    parties: list[str] = []
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    governing_law: Optional[str] = None
    total_value: Optional[str] = None


class SearchQuery(BaseModel):
    query: str
    document_ids: Optional[list[str]] = None  # None = search all
    top_k: int = 5


class SearchResult(BaseModel):
    answer: str
    citations: list[dict]  # [{document_id, chunk_text, relevance_score, section}]
    confidence: float


class ComparisonResult(BaseModel):
    doc_a_id: str
    doc_b_id: str
    changes: list[dict]  # [{type: added|removed|modified, clause, detail, risk_impact}]
    summary: str
    new_risks: list[str] = []


class AuditLogEntry(BaseModel):
    id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str  # upload, classify, extract, search, compare
    document_id: Optional[str] = None
    user_id: str = "demo_user"
    input_summary: str = ""
    output_summary: str = ""
    model_used: str = ""
    latency_ms: int = 0
    confidence: Optional[float] = None
