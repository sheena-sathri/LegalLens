"""Document classification using Claude."""

from app.llm.client import call_claude_json
from app.llm.prompts import CLASSIFIER_SYSTEM
from app.llm.context_engineer import assemble_classification_context
from app.db.metadata_store import get_document, update_document_classification, log_audit


async def classify_document(document_id: str) -> dict:
    """
    Classify a document using Claude.

    Returns classification result with type, confidence, and metadata.
    """
    # Get document text
    doc = await get_document(document_id)
    if not doc:
        raise ValueError(f"Document {document_id} not found")

    raw_text = doc["raw_text"]

    # Assemble context (handles truncation for long docs)
    context = assemble_classification_context(raw_text)

    # Call Claude
    result = call_claude_json(
        system_prompt=CLASSIFIER_SYSTEM,
        user_message=f"Classify this legal document:\n\n{context}",
    )

    classification = result["parsed"]

    # Save to DB
    await update_document_classification(document_id, classification)

    # Audit log
    await log_audit(
        action="classify",
        document_id=document_id,
        input_summary=f"Classified {doc['filename']}",
        output_summary=f"{classification.get('document_type', 'Unknown')} ({classification.get('confidence', 0):.0%})",
        model_used=result["model"],
        latency_ms=result["latency_ms"],
        confidence=classification.get("confidence"),
    )

    return {
        "document_id": document_id,
        "classification": classification,
        "usage": result["usage"],
        "latency_ms": result["latency_ms"],
    }
