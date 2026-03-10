"""Clause extraction and risk assessment using Claude."""

import json
from typing import Optional

from app.llm.client import call_claude_json
from app.llm.prompts import CLAUSE_EXTRACTOR_SYSTEM
from app.llm.context_engineer import assemble_extraction_context
from app.db.metadata_store import get_document, save_extraction, log_audit


DEFAULT_PLAYBOOK = {
    "Limitation of Liability": {
        "preferred": "Mutual cap at 2x annual contract value",
        "fallback": "Mutual cap at 1x annual contract value",
        "red_line": "No uncapped liability; no unlimited indemnification"
    },
    "Termination": {
        "preferred": "Mutual termination for convenience with 90 days notice",
        "fallback": "60 days notice acceptable",
        "red_line": "Must have termination for cause provision"
    },
    "Indemnification": {
        "preferred": "Mutual indemnification for IP infringement and breach",
        "fallback": "Vendor indemnifies for IP; mutual for breach",
        "red_line": "No one-sided indemnification without cap"
    },
    "Confidentiality": {
        "preferred": "Mutual NDA with 3-year survival period",
        "fallback": "2-year survival acceptable",
        "red_line": "Must include carve-outs for legally compelled disclosure"
    },
    "Data Protection": {
        "preferred": "GDPR and CCPA compliant; data processing agreement required",
        "fallback": "Contractual data protection commitments",
        "red_line": "No unlimited right to use customer data"
    },
    "IP Assignment": {
        "preferred": "Customer owns all work product; vendor retains pre-existing IP with license",
        "fallback": "Joint ownership with exclusive license",
        "red_line": "Vendor cannot own customer-specific deliverables"
    }
}


async def extract_clauses(document_id: str,
                           playbook: Optional[dict] = None) -> dict:
    """
    Extract and assess clauses from a document.

    Args:
        document_id: The document to analyze
        playbook: Optional contract playbook. Uses default if not provided.

    Returns extraction result with clauses, risk levels, and summary.
    """
    doc = await get_document(document_id)
    if not doc:
        raise ValueError(f"Document {document_id} not found")

    raw_text = doc["raw_text"]
    pb = playbook or DEFAULT_PLAYBOOK

    # Assemble context with playbook
    context = assemble_extraction_context(raw_text, pb)

    result = call_claude_json(
        system_prompt=CLAUSE_EXTRACTOR_SYSTEM,
        user_message=f"Extract and assess all key clauses from this document:\n\n{context}",
        max_tokens=8192,  # Extraction can be verbose
    )

    extraction = result["parsed"]

    # Save extraction
    await save_extraction(
        document_id=document_id,
        clauses=extraction.get("clauses", []),
        metadata=extraction.get("metadata", {}),
        summary=extraction.get("summary", ""),
    )

    # Audit log
    clause_count = len(extraction.get("clauses", []))
    risk_dist = extraction.get("metadata", {}).get("risk_distribution", {})
    await log_audit(
        action="extract",
        document_id=document_id,
        input_summary=f"Extracted clauses from {doc['filename']}",
        output_summary=f"{clause_count} clauses found. Risks: {json.dumps(risk_dist)}",
        model_used=result["model"],
        latency_ms=result["latency_ms"],
    )

    return {
        "document_id": document_id,
        "extraction": extraction,
        "usage": result["usage"],
        "latency_ms": result["latency_ms"],
    }
