"""SQLite metadata store for documents and audit logs."""

import aiosqlite
import json
from datetime import datetime
from typing import Optional

_db_path: str = ""


async def init_db(db_path: str):
    """Initialize the SQLite database with required tables."""
    global _db_path
    _db_path = db_path

    async with aiosqlite.connect(_db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                page_count INTEGER DEFAULT 0,
                character_count INTEGER DEFAULT 0,
                raw_text TEXT,
                classification TEXT,  -- JSON
                metadata TEXT,        -- JSON
                status TEXT DEFAULT 'uploaded',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                document_id TEXT,
                user_id TEXT DEFAULT 'demo_user',
                input_summary TEXT,
                output_summary TEXT,
                model_used TEXT,
                latency_ms INTEGER DEFAULT 0,
                confidence REAL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS extractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                clauses TEXT NOT NULL,  -- JSON
                metadata TEXT,          -- JSON
                summary TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(document_id)
            )
        """)

        await db.commit()
    print(f"  📦 SQLite initialized at {db_path}")


async def save_document(document_id: str, filename: str, file_type: str,
                        page_count: int, character_count: int, raw_text: str):
    async with aiosqlite.connect(_db_path) as db:
        await db.execute(
            """INSERT INTO documents (document_id, filename, file_type, page_count, character_count, raw_text)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (document_id, filename, file_type, page_count, character_count, raw_text)
        )
        await db.commit()


async def get_document(document_id: str) -> Optional[dict]:
    async with aiosqlite.connect(_db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM documents WHERE document_id = ?", (document_id,))
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return None


async def update_document_classification(document_id: str, classification: dict):
    async with aiosqlite.connect(_db_path) as db:
        await db.execute(
            "UPDATE documents SET classification = ?, updated_at = ? WHERE document_id = ?",
            (json.dumps(classification), datetime.utcnow().isoformat(), document_id)
        )
        await db.commit()


async def save_extraction(document_id: str, clauses: list, metadata: dict, summary: str):
    async with aiosqlite.connect(_db_path) as db:
        await db.execute(
            """INSERT INTO extractions (document_id, clauses, metadata, summary)
               VALUES (?, ?, ?, ?)""",
            (document_id, json.dumps(clauses), json.dumps(metadata), summary)
        )
        await db.commit()


async def list_documents() -> list[dict]:
    async with aiosqlite.connect(_db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT document_id, filename, file_type, page_count, classification, status, created_at FROM documents ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def log_audit(action: str, document_id: str = None, input_summary: str = "",
                    output_summary: str = "", model_used: str = "",
                    latency_ms: int = 0, confidence: float = None):
    async with aiosqlite.connect(_db_path) as db:
        await db.execute(
            """INSERT INTO audit_logs (action, document_id, input_summary, output_summary, model_used, latency_ms, confidence)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (action, document_id, input_summary, output_summary, model_used, latency_ms, confidence)
        )
        await db.commit()


async def get_audit_logs(limit: int = 100) -> list[dict]:
    async with aiosqlite.connect(_db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
