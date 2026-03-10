"""Text chunking strategies for legal documents.

Legal documents have structure (sections, clauses, sub-clauses) that should be
respected when chunking. Naive token-based chunking can split a clause in half,
losing critical context. This module provides section-aware chunking.
"""

import re
from typing import Optional


# Common legal section patterns
SECTION_PATTERNS = [
    r"(?m)^(?:ARTICLE|Article)\s+[IVXLCDM\d]+[.\s]",       # ARTICLE I, Article 1
    r"(?m)^(?:SECTION|Section)\s+\d+[.\d]*[.\s]",           # SECTION 1, Section 1.2
    r"(?m)^\d+\.\s+[A-Z]",                                   # 1. Capital letter start
    r"(?m)^\d+\.\d+\s+",                                     # 1.1 Sub-section
    r"(?m)^[A-Z][A-Z\s]{5,}$",                              # ALL CAPS HEADERS
    r"(?m)^(?:WHEREAS|NOW, THEREFORE|IN WITNESS WHEREOF)",   # Legal boilerplate markers
]


def chunk_by_sections(text: str, max_chunk_size: int = 1000,
                      overlap: int = 200) -> list[dict]:
    """
    Chunk text respecting legal document section boundaries.

    Strategy:
    1. Try to split on section/clause boundaries first
    2. If a section exceeds max_chunk_size, split on paragraph boundaries
    3. As a last resort, split on sentence boundaries

    Returns list of {text, chunk_index, section}
    """
    # Find section boundaries
    boundaries = _find_section_boundaries(text)

    if not boundaries:
        # No clear sections — fall back to paragraph-based chunking
        return chunk_by_paragraphs(text, max_chunk_size, overlap)

    chunks = []
    for i, (start, end, section_title) in enumerate(boundaries):
        section_text = text[start:end].strip()

        if len(section_text) <= max_chunk_size:
            chunks.append({
                "text": section_text,
                "chunk_index": len(chunks),
                "section": section_title,
            })
        else:
            # Section too large — split by paragraphs within it
            sub_chunks = chunk_by_paragraphs(section_text, max_chunk_size, overlap)
            for sc in sub_chunks:
                sc["section"] = section_title
                sc["chunk_index"] = len(chunks)
                chunks.append(sc)

    return chunks


def chunk_by_paragraphs(text: str, max_chunk_size: int = 1000,
                        overlap: int = 200) -> list[dict]:
    """
    Chunk text by paragraph boundaries with overlap.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_chunk = ""
    current_start = 0

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_chunk_size and current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "chunk_index": len(chunks),
                "section": "",
            })
            # Overlap: keep tail of current chunk
            if overlap > 0:
                current_chunk = current_chunk[-overlap:] + "\n\n" + para
            else:
                current_chunk = para
        else:
            current_chunk = current_chunk + "\n\n" + para if current_chunk else para

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "chunk_index": len(chunks),
            "section": "",
        })

    return chunks


def chunk_by_sentences(text: str, max_chunk_size: int = 1000,
                       overlap_sentences: int = 2) -> list[dict]:
    """
    Chunk text by sentence boundaries — last resort fallback.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_sentences = []
    current_len = 0

    for sentence in sentences:
        if current_len + len(sentence) > max_chunk_size and current_sentences:
            chunks.append({
                "text": " ".join(current_sentences),
                "chunk_index": len(chunks),
                "section": "",
            })
            # Overlap
            current_sentences = current_sentences[-overlap_sentences:]
            current_len = sum(len(s) for s in current_sentences)

        current_sentences.append(sentence)
        current_len += len(sentence)

    if current_sentences:
        chunks.append({
            "text": " ".join(current_sentences),
            "chunk_index": len(chunks),
            "section": "",
        })

    return chunks


def _find_section_boundaries(text: str) -> list[tuple[int, int, str]]:
    """
    Find section start/end positions and titles in the text.
    Returns list of (start_pos, end_pos, section_title).
    """
    all_matches = []

    for pattern in SECTION_PATTERNS:
        for match in re.finditer(pattern, text):
            # Extract section title (first line of the match)
            line_end = text.find("\n", match.start())
            if line_end == -1:
                line_end = len(text)
            title = text[match.start():line_end].strip()[:100]
            all_matches.append((match.start(), title))

    if len(all_matches) < 2:
        return []

    # Sort by position
    all_matches.sort(key=lambda x: x[0])

    # Convert to boundaries (start, end, title)
    boundaries = []
    for i in range(len(all_matches)):
        start = all_matches[i][0]
        end = all_matches[i + 1][0] if i + 1 < len(all_matches) else len(text)
        title = all_matches[i][1]
        boundaries.append((start, end, title))

    return boundaries
