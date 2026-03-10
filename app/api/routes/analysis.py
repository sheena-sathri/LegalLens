"""Analysis API routes — classification, extraction, comparison."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.classifier import classify_document
from app.core.clause_extractor import extract_clauses
from app.core.comparator import compare_documents

router = APIRouter()


@router.post("/classify/{document_id}")
async def classify(document_id: str):
    """Classify a document by type (NDA, MSA, SOW, etc.)."""
    try:
        result = await classify_document(document_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@router.post("/extract/{document_id}")
async def extract(document_id: str):
    """Extract key clauses and assess risks for a document."""
    try:
        result = await extract_clauses(document_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


class CompareRequest(BaseModel):
    doc_a_id: str
    doc_b_id: str


@router.post("/compare")
async def compare(request: CompareRequest):
    """Compare two document versions and identify changes."""
    try:
        result = await compare_documents(request.doc_a_id, request.doc_b_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
