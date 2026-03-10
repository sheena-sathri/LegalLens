"""Text processing utilities for cleaning and normalizing legal document text."""

import re


def clean_text(text: str) -> str:
    """Clean extracted text from PDF/DOCX artifacts."""
    # Remove excessive whitespace but preserve paragraph breaks
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'(?m)^Page \d+ of \d+$', '', text)
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Standalone page numbers

    # Remove non-printable characters (except newlines)
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    return text.strip()


def extract_parties(text: str) -> list[str]:
    """Attempt to extract party names from contract text."""
    parties = []

    # Common patterns: "between X and Y", "by and between X and Y"
    patterns = [
        r'(?i)between\s+(.+?)\s+(?:and|&)\s+(.+?)(?:\.|,|\()',
        r'(?i)(?:this agreement|this contract).+?(?:between|by and between)\s+(.+?)\s+(?:and|&)\s+(.+?)(?:\.|,|\()',
        r'(?i)"([^"]+)"\s*\((?:the\s+)?"(?:Company|Client|Vendor|Contractor|Party)"\)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text[:3000])  # Only check first part
        for match in matches:
            if isinstance(match, tuple):
                parties.extend([p.strip().strip('"\'') for p in match if p.strip()])
            else:
                parties.append(match.strip().strip('"\''))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in parties:
        if p.lower() not in seen and len(p) > 2:
            seen.add(p.lower())
            unique.append(p)

    return unique[:4]  # Max 4 parties


def extract_dates(text: str) -> dict:
    """Extract key dates from contract text."""
    dates = {}

    # Effective date patterns
    eff_patterns = [
        r'(?i)effective\s+(?:as\s+of\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
        r'(?i)effective\s+(?:as\s+of\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)dated\s+(?:as\s+of\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
    ]

    for pattern in eff_patterns:
        match = re.search(pattern, text[:5000])
        if match:
            dates["effective_date"] = match.group(1).strip()
            break

    # Expiration / termination date
    exp_patterns = [
        r'(?i)(?:expire|expiration|termination\s+date)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})',
        r'(?i)(?:expire|expiration|termination\s+date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)term\s+of\s+(\d+)\s+(year|month|day)',
    ]

    for pattern in exp_patterns:
        match = re.search(pattern, text)
        if match:
            dates["expiration_date"] = match.group(0).strip()
            break

    return dates


def truncate_for_context(text: str, max_chars: int = 100000) -> str:
    """Truncate text to fit within context window limits."""
    if len(text) <= max_chars:
        return text
    # Keep beginning and end (legal docs often have key terms at both ends)
    half = max_chars // 2
    return text[:half] + "\n\n[...truncated...]\n\n" + text[-half:]
