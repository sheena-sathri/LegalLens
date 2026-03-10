"""Search / RAG Q&A API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.rag_engine import ask_question

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    document_ids: Optional[list[str]] = None
    top_k: int = 5


@router.post("/ask")
async def search_ask(request: SearchRequest):
    """Ask a natural language question about your documents."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = await ask_question(
            query=request.query,
            document_ids=request.document_ids,
            top_k=request.top_k,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
