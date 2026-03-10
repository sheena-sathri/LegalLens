"""Context engineering for LegalLens.

Manages context window assembly for different tasks, ensuring optimal
use of Claude's context window by dynamically selecting and ordering
relevant content.
"""

import tiktoken
from typing import Optional


# Approximate token budget for Claude Sonnet (leaving room for system prompt + output)
MAX_CONTEXT_TOKENS = 150000
SYSTEM_PROMPT_BUDGET = 2000
OUTPUT_BUDGET = 4096
AVAILABLE_BUDGET = MAX_CONTEXT_TOKENS - SYSTEM_PROMPT_BUDGET - OUTPUT_BUDGET


def estimate_tokens(text: str) -> int:
    """Estimate token count for a text string."""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        # Fallback: rough estimate of 4 chars per token
        return len(text) // 4


def assemble_classification_context(document_text: str) -> str:
    """
    Assemble context for document classification.
    Strategy: Use as much of the document as fits, prioritizing
    the beginning (where document type is usually declared) and
    the end (where signatures and governing terms often appear).
    """
    tokens = estimate_tokens(document_text)

    if tokens <= AVAILABLE_BUDGET:
        return document_text

    # Split budget: 60% beginning, 40% end
    char_budget = AVAILABLE_BUDGET * 4  # rough chars estimate
    begin_budget = int(char_budget * 0.6)
    end_budget = int(char_budget * 0.4)

    return (
        document_text[:begin_budget]
        + "\n\n[...document truncated for context window...]\n\n"
        + document_text[-end_budget:]
    )


def assemble_extraction_context(document_text: str,
                                 playbook: Optional[dict] = None) -> str:
    """
    Assemble context for clause extraction.
    Includes the full document (truncated if needed) plus optional playbook.
    """
    parts = []

    if playbook:
        playbook_text = format_playbook(playbook)
        parts.append(f"=== Organization Playbook ===\n{playbook_text}\n")

    parts.append(f"=== Document to Analyze ===\n{document_text}")

    full_context = "\n\n".join(parts)
    tokens = estimate_tokens(full_context)

    if tokens <= AVAILABLE_BUDGET:
        return full_context

    # Truncate document, keep playbook intact
    playbook_tokens = estimate_tokens(parts[0]) if playbook else 0
    doc_budget = (AVAILABLE_BUDGET - playbook_tokens) * 4

    truncated_doc = document_text[:doc_budget]
    parts[-1] = f"=== Document to Analyze (truncated) ===\n{truncated_doc}"

    return "\n\n".join(parts)


def assemble_rag_context(query: str, chunks: list[dict],
                          max_chunks: int = 10) -> str:
    """
    Assemble context for RAG Q&A.
    Strategy: Include top-k chunks sorted by relevance, fitting within budget.
    """
    # Sort by relevance score (highest first)
    sorted_chunks = sorted(chunks, key=lambda c: c.get("relevance_score", 0), reverse=True)

    selected_chunks = []
    total_tokens = estimate_tokens(query) + 500  # query + overhead

    for chunk in sorted_chunks[:max_chunks]:
        chunk_tokens = estimate_tokens(chunk.get("text", ""))
        if total_tokens + chunk_tokens > AVAILABLE_BUDGET:
            break
        selected_chunks.append(chunk)
        total_tokens += chunk_tokens

    return selected_chunks


def assemble_comparison_context(text_a: str, text_b: str) -> tuple[str, str]:
    """
    Assemble context for document comparison.
    If both documents are too large, truncate proportionally.
    """
    total_tokens = estimate_tokens(text_a) + estimate_tokens(text_b)

    if total_tokens <= AVAILABLE_BUDGET:
        return text_a, text_b

    # Split budget equally
    half_budget = (AVAILABLE_BUDGET * 4) // 2
    return text_a[:half_budget], text_b[:half_budget]


def format_playbook(playbook: dict) -> str:
    """Format a contract playbook into readable context."""
    lines = []
    for category, rules in playbook.items():
        lines.append(f"\n## {category}")
        if isinstance(rules, list):
            for rule in rules:
                lines.append(f"  - {rule}")
        elif isinstance(rules, dict):
            for key, value in rules.items():
                lines.append(f"  - {key}: {value}")
        else:
            lines.append(f"  {rules}")
    return "\n".join(lines)
