"""Governance and audit trail service."""

from app.db.metadata_store import get_audit_logs


async def get_audit_trail(limit: int = 100) -> list[dict]:
    """Get recent audit log entries."""
    return await get_audit_logs(limit=limit)


async def export_audit_report() -> dict:
    """Generate an audit report summary."""
    logs = await get_audit_logs(limit=1000)

    # Aggregate stats
    action_counts = {}
    total_latency = 0
    total_calls = 0

    for log in logs:
        action = log.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
        if log.get("latency_ms"):
            total_latency += log["latency_ms"]
            total_calls += 1

    avg_latency = total_latency / total_calls if total_calls > 0 else 0

    return {
        "total_operations": len(logs),
        "action_breakdown": action_counts,
        "average_latency_ms": round(avg_latency),
        "logs": logs[:100],  # Return last 100 for display
    }
