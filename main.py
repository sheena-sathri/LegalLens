"""LegalLens — AI-Powered Legal Document Intelligence Platform"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import get_settings
from app.db.metadata_store import init_db
from app.db.vector_store import init_vector_store
from app.api.routes import documents, analysis, search, governance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup, cleanup on shutdown."""
    settings = get_settings()
    await init_db(settings.sqlite_db_path)
    init_vector_store(settings.chroma_persist_dir)
    print("✅ LegalLens initialized")
    yield
    print("👋 LegalLens shutting down")


app = FastAPI(
    title="LegalLens",
    description="AI-Powered Legal Document Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(governance.router, prefix="/api/v1/governance", tags=["Governance"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "LegalLens", "version": "0.1.0"}
