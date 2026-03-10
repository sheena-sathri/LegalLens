"""ChromaDB vector store for document embeddings and retrieval."""

import chromadb
from typing import Optional
import os

_client: Optional[chromadb.ClientAPI] = None
_collection: Optional[chromadb.Collection] = None

COLLECTION_NAME = "legallens_documents"


def init_vector_store(persist_dir: str):
    """Initialize ChromaDB with persistence."""
    global _client, _collection

    os.makedirs(persist_dir, exist_ok=True)
    _client = chromadb.PersistentClient(path=persist_dir)

    _collection = _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"  ChromaDB initialized - {_collection.count()} chunks indexed")


def get_collection() -> chromadb.Collection:
    if _collection is None:
        raise RuntimeError("Vector store not initialized. Call init_vector_store() first.")
    return _collection


def add_document_chunks(document_id: str, chunks: list[dict]):
    """
    Add document chunks to the vector store.

    Args:
        document_id: Unique document identifier
        chunks: List of dicts with keys: {text, chunk_index, section, metadata}
    """
    collection = get_collection()

    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "document_id": document_id,
            "chunk_index": chunk.get("chunk_index", i),
            "section": chunk.get("section", ""),
            **chunk.get("metadata", {})
        }
        for i, chunk in enumerate(chunks)
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )
    return len(ids)


def search_documents(query: str, top_k: int = 5,
                     document_ids: Optional[list[str]] = None) -> list[dict]:
    """
    Search for relevant document chunks.

    Args:
        query: Natural language search query
        top_k: Number of results to return
        document_ids: Optional filter to specific documents

    Returns:
        List of {text, document_id, chunk_index, section, relevance_score}
    """
    collection = get_collection()

    where_filter = None
    if document_ids:
        if len(document_ids) == 1:
            where_filter = {"document_id": document_ids[0]}
        else:
            where_filter = {"document_id": {"$in": document_ids}}

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter,
    )

    search_results = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            search_results.append({
                "text": doc,
                "document_id": results["metadatas"][0][i].get("document_id", ""),
                "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
                "section": results["metadatas"][0][i].get("section", ""),
                "relevance_score": 1 - (results["distances"][0][i] if results["distances"] else 0),
            })

    return search_results


def delete_document_chunks(document_id: str):
    """Remove all chunks for a document."""
    collection = get_collection()
    # Get all chunk IDs for this document
    results = collection.get(where={"document_id": document_id})
    if results["ids"]:
        collection.delete(ids=results["ids"])
    return len(results["ids"]) if results["ids"] else 0


def get_document_chunk_count(document_id: str) -> int:
    """Get number of chunks indexed for a document."""
    collection = get_collection()
    results = collection.get(where={"document_id": document_id})
    return len(results["ids"]) if results["ids"] else 0
