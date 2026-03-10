"""Governance and audit trail API routes."""

from fastapi import APIRouter
from app.core.governance import get_audit_trail, export_audit_report

router = APIRouter()


@router.get("/audit")
async def audit_trail(limit: int = 100):
    """Get recent audit log entries."""
    logs = await get_audit_trail(limit=limit)
    return {"logs": logs, "total": len(logs)}


@router.get("/audit/report")
async def audit_report():
    """Generate an audit report summary."""
    report = await export_audit_report()
    return report
