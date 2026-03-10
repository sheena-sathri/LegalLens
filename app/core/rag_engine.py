"""RAG (Retrieval-Augmented Generation) engine for document Q&A."""

from typing import Optional

from app.llm.client import call_claude_json
from app.llm.prompts import RAG_QA_SYSTEM, build_rag_context
from app.llm.context_engineer import assemble_rag_context
from app.db.vector_store import search_documents
from app.db.metadata_store import log_audit


async def ask_question(query: str,
                        document_ids: Optional[list[str]] = None,
                        top_k: int = 5) -> dict:
    """
    Answer a question using RAG over the document knowledge base.

    Pipeline:
    1. Retrieve relevant chunks from ChromaDB
    2. Assemble context with retrieved chunks
    3. Generate answer with Claude
    4. Return answer with citations

    Args:
        query: Natural language question
        document_ids: Optional filter to specific documents
        top_k: Number of chunks to retrieve

    Returns:
        Answer with citations and confidence score
    """
    # Step 1: Retrieve
    raw_chunks = search_documents(
        query=query,
        top_k=top_k * 2,  # Retrieve more, then filter by budget
        document_ids=document_ids,
    )

    if not raw_chunks:
        return {
            "answer": "No relevant documents found in the knowledge base. Please upload documents first.",
            "citations": [],
            "confidence": 0.0,
            "chunks_retrieved": 0,
        }

    # Step 2: Assemble context (respects token budget)
    selected_chunks = assemble_rag_context(query, raw_chunks, max_chunks=top_k)

    # Step 3: Build prompt and generate
    context_str = build_rag_context(query, selected_chunks)

    result = call_claude_json(
        system_prompt=RAG_QA_SYSTEM,
        user_message=context_str,
    )

    answer_data = result["parsed"]

    # Step 4: Audit log
    await log_audit(
        action="search",
        input_summary=f"Q: {query[:200]}",
        output_summary=f"A: {answer_data.get('answer', '')[:200]}",
        model_used=result["model"],
        latency_ms=result["latency_ms"],
        confidence=answer_data.get("confidence"),
    )

    return {
        "answer": answer_data.get("answer", ""),
        "citations": answer_data.get("citations", []),
        "confidence": answer_data.get("confidence", 0.0),
        "caveats": answer_data.get("caveats", ""),
        "chunks_retrieved": len(selected_chunks),
        "usage": result["usage"],
        "latency_ms": result["latency_ms"],
    }
