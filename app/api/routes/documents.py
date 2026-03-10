"""Document management API routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.document_processor import process_document
from app.db.metadata_store import list_documents, get_document, log_audit

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a legal document (PDF, DOCX, or TXT)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    allowed = {".pdf", ".docx", ".doc", ".txt"}
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: {allowed}")

    try:
        result = await process_document(file.file, file.filename)
        await log_audit(
            action="upload",
            document_id=result["document_id"],
            input_summary=f"Uploaded {file.filename}",
            output_summary=f"{result['page_count']} pages, {result['chunks_indexed']} chunks indexed",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.get("/")
async def list_all_documents():
    """List all uploaded documents."""
    docs = await list_documents()
    return {"documents": docs, "total": len(docs)}


@router.get("/{document_id}")
async def get_document_details(document_id: str):
    """Get details for a specific document."""
    doc = await get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    # Don't return raw_text in list view (too large)
    doc.pop("raw_text", None)
    return doc
