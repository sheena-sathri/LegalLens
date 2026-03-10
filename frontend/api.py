"""API helper functions for LegalLens frontend."""

import os
import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8001/api/v1")


def api_get(endpoint: str):
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post(endpoint: str, json_data: dict = None, files: dict = None):
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=json_data, files=files, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def get_documents():
    result = api_get("/documents/")
    return result.get("documents", []) if result else []
