"""Contract comparison service."""

from app.llm.client import call_claude_json
from app.llm.prompts import COMPARATOR_SYSTEM, build_comparison_context
from app.llm.context_engineer import assemble_comparison_context
from app.db.metadata_store import get_document, log_audit


async def compare_documents(doc_a_id: str, doc_b_id: str) -> dict:
    """
    Compare two versions of a document and identify meaningful changes.

    Args:
        doc_a_id: Original document ID
        doc_b_id: Revised document ID

    Returns comparison result with changes, risk impacts, and recommendations.
    """
    doc_a = await get_document(doc_a_id)
    doc_b = await get_document(doc_b_id)

    if not doc_a:
        raise ValueError(f"Document {doc_a_id} not found")
    if not doc_b:
        raise ValueError(f"Document {doc_b_id} not found")

    # Assemble context (handles truncation)
    text_a, text_b = assemble_comparison_context(doc_a["raw_text"], doc_b["raw_text"])
    context = build_comparison_context(
        text_a, text_b,
        label_a=doc_a["filename"],
        label_b=doc_b["filename"],
    )

    result = call_claude_json(
        system_prompt=COMPARATOR_SYSTEM,
        user_message=f"Compare these two document versions:\n\n{context}",
        max_tokens=8192,
    )

    comparison = result["parsed"]

    # Audit log
    num_changes = len(comparison.get("changes", []))
    await log_audit(
        action="compare",
        document_id=f"{doc_a_id} vs {doc_b_id}",
        input_summary=f"Compared {doc_a['filename']} vs {doc_b['filename']}",
        output_summary=f"{num_changes} meaningful changes found",
        model_used=result["model"],
        latency_ms=result["latency_ms"],
    )

    return {
        "doc_a_id": doc_a_id,
        "doc_b_id": doc_b_id,
        "comparison": comparison,
        "usage": result["usage"],
        "latency_ms": result["latency_ms"],
    }
