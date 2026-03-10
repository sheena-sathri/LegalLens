"""Tool definitions for Claude tool use.

These tools allow Claude to interact with the LegalLens system
during complex queries — e.g., searching across documents,
looking up specific clauses, checking the playbook.
"""

TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search the legal document knowledge base for relevant information. Use this when answering questions that require finding specific content across multiple documents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant document chunks"
                },
                "document_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of specific document IDs to search within. If empty, searches all documents."
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return (default 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_document_metadata",
        "description": "Retrieve metadata and classification for a specific document, including parties, dates, document type, and risk summary.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The document ID to look up"
                }
            },
            "required": ["document_id"]
        }
    },
    {
        "name": "get_clause_details",
        "description": "Get detailed extraction results for a specific document, including all identified clauses and their risk assessments.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The document ID to get clause details for"
                },
                "clause_type": {
                    "type": "string",
                    "description": "Optional filter for a specific clause type (e.g., 'Termination', 'Liability')"
                }
            },
            "required": ["document_id"]
        }
    },
    {
        "name": "check_playbook",
        "description": "Check the organization's contract playbook for guidance on a specific clause type or negotiation scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to look up in the playbook (e.g., 'liability cap', 'termination notice period')"
                }
            },
            "required": ["topic"]
        }
    }
]
