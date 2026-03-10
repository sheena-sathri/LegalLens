"""LegalLens — Legal AI Hub — Streamlit Frontend"""

import streamlit as st
import json
import time
from datetime import datetime, date, timedelta

import plotly.express as px
import plotly.graph_objects as go

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import api_get, api_post, get_documents
from mock_data import (
    MATTERS, RECENT_REQUESTS, HISTORICAL_DATA, MATTERS_BY_TYPE,
    RISK_DISTRIBUTION, WORKLOAD, AVG_RESPONSE_BY_TYPE, ASSIGNEES,
    SLACK_CONVERSATION, EMAIL_INTAKE, INTEGRATIONS,
)

st.set_page_config(
    page_title="LegalLens",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#4F46E5",
    "primary_light": "#6366F1",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "orange": "#F97316",
    "bg_dark": "#1E1E2E",
    "bg_card": "#FFFFFF",
    "text": "#1F2937",
    "text_muted": "#6B7280",
    "border": "#E5E7EB",
}

PRIORITY_COLORS = {
    "Low": COLORS["success"],
    "Medium": COLORS["warning"],
    "High": COLORS["orange"],
    "Urgent": COLORS["danger"],
}

STATUS_COLORS = {
    "New": "#6366F1",
    "Triaged": "#8B5CF6",
    "In Progress": "#3B82F6",
    "In Review": "#3B82F6",
    "Pending Approval": COLORS["warning"],
    "Approved": COLORS["success"],
    "Closed": "#6B7280",
    "Resolved": COLORS["success"],
}

st.markdown("""
<style>
    :root {
        color-scheme: light !important;
    }
    .main .block-container, .main .block-container * {
        color: #000000;
    }
    .main .block-container .stMarkdown div[data-testid="stMarkdownContainer"] p,
    .main .block-container .stMarkdown div[data-testid="stMarkdownContainer"] h1,
    .main .block-container .stMarkdown div[data-testid="stMarkdownContainer"] h2,
    .main .block-container .stMarkdown div[data-testid="stMarkdownContainer"] h3 {
        color: #000000 !important;
    }
    iframe[title="st.markdown"] {
        color-scheme: light !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1E2E 0%, #2D2B55 100%);
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #E2E8F0 !important;
        font-size: 0.95rem;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(99, 102, 241, 0.15);
        border-radius: 8px;
    }
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1F2937;
    }
    .metric-card .metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        margin-top: 0.25rem;
    }
    .kanban-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.85rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s;
    }
    .kanban-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .kanban-card .card-id {
        font-size: 0.7rem;
        color: #9CA3AF;
        font-family: monospace;
    }
    .kanban-card .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1F2937;
        margin: 0.25rem 0;
        line-height: 1.3;
    }
    .kanban-card .card-meta {
        font-size: 0.72rem;
        color: #6B7280;
        margin-top: 0.4rem;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-right: 4px;
    }
    .chat-user {
        background: #EEF2FF;
        border-radius: 16px 16px 4px 16px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        color: #1F2937;
    }
    .chat-bot {
        background: #F3F4F6;
        border-radius: 16px 16px 16px 4px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        color: #1F2937;
    }
    .slack-bubble {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        margin: 0.4rem 0;
    }
    .slack-bubble .slack-user {
        font-weight: 700;
        font-size: 0.85rem;
        color: #1F2937;
    }
    .slack-bubble .slack-time {
        font-size: 0.7rem;
        color: #9CA3AF;
        margin-left: 0.5rem;
    }
    .slack-bubble .slack-msg {
        font-size: 0.85rem;
        color: #374151;
        margin-top: 0.2rem;
        line-height: 1.5;
    }
    .request-feed-item {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-left: 4px solid;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    .flow-step {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        color: #1F2937 !important;
    }
    .flow-step div, .flow-step span {
        color: inherit !important;
    }
    .integration-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        color: #1F2937 !important;
    }
    .integration-card div, .integration-card span {
        color: inherit !important;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #000000 !important;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .footer-bar {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #9CA3AF;
        font-size: 0.8rem;
        border-top: 1px solid #E5E7EB;
        margin-top: 3rem;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


def render_badge(text, color):
    return f'<span class="badge" style="background:{color};">{text}</span>'


def render_status_badge(status):
    color = STATUS_COLORS.get(status, "#6B7280")
    return render_badge(status, color)


def render_priority_badge(priority):
    color = PRIORITY_COLORS.get(priority, "#6B7280")
    return render_badge(priority, color)


def render_metric_card(value, label, color=COLORS["primary"]):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="footer-bar">
        LegalLens — AI-Powered Legal Intelligence Platform | Built for enterprise legal teams that demand privacy-first AI.
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size:2rem;">⚖️</div>
        <div style="font-size:1.4rem; font-weight:800; letter-spacing:-0.5px;">LegalLens</div>
        <div style="font-size:0.8rem; color:#A5B4FC; margin-top:2px;">Legal AI Hub</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigation",
        [
            "🚪 AI Front Door",
            "📋 Matter Management",
            "💬 AI Assistant",
            "📄 Document Intelligence",
            "📊 Dashboard",
            "🔒 Privacy & Safety",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("© 2024 LegalLens · v2.0")


# ════════════════════════════════════════════════════════════
# 1. AI FRONT DOOR
# ════════════════════════════════════════════════════════════
if page == "🚪 AI Front Door":
    st.markdown("## 🚪 AI Front Door")
    st.markdown("Submit a legal request in natural language. LegalLens will classify, route, and track it automatically.")

    col_intake, col_right = st.columns([3, 2])

    with col_intake:
        st.markdown('<div class="section-header">New Request</div>', unsafe_allow_html=True)
        user_request = st.text_area(
            "Describe your legal request",
            placeholder="e.g., I need an NDA reviewed for a new vendor partnership with TechFlow Solutions...",
            height=120,
            label_visibility="collapsed",
        )

        qc1, qc2, qc3, qc4 = st.columns(4)
        with qc1:
            if st.button("📝 Request NDA", use_container_width=True):
                st.session_state["front_door_input"] = "I need a mutual NDA drafted for a new vendor."
        with qc2:
            if st.button("❓ Policy Question", use_container_width=True):
                st.session_state["front_door_input"] = "What is our policy on remote work for contractors?"
        with qc3:
            if st.button("📄 Contract Review", use_container_width=True):
                st.session_state["front_door_input"] = "Please review the attached MSA from our cloud provider."
        with qc4:
            if st.button("🚨 Report an Issue", use_container_width=True):
                st.session_state["front_door_input"] = "I need to report a potential compliance issue with a vendor."

        if st.button("🚀 Submit Request", type="primary", use_container_width=True) and user_request:
            with st.spinner("🤖 Classifying your request..."):
                result = api_post("/search/ask", json_data={"query": user_request, "top_k": 3})
                time.sleep(0.5)

            st.success("✅ Request submitted and classified!")
            rc1, rc2, rc3, rc4 = st.columns(4)
            with rc1:
                render_metric_card("NDA Review", "Matter Type", COLORS["primary"])
            with rc2:
                render_metric_card("94%", "Confidence", COLORS["success"])
            with rc3:
                render_metric_card("High", "Urgency", COLORS["orange"])
            with rc4:
                render_metric_card("Contracts", "Routed To", COLORS["primary"])

            if result and result.get("answer"):
                with st.expander("💡 AI Analysis", expanded=True):
                    st.markdown(result["answer"])

        st.markdown('<div class="section-header">Recent Requests</div>', unsafe_allow_html=True)
        for req in RECENT_REQUESTS:
            urgency_color = PRIORITY_COLORS.get(req["urgency"], "#6B7280")
            status_color = STATUS_COLORS.get(req["status"], "#6B7280")
            st.markdown(f"""
            <div class="request-feed-item" style="border-left-color: {urgency_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-weight:600; font-size:0.85rem; color:#1F2937;">{req["request"]}</div>
                    <div>{render_status_badge(req["status"])}</div>
                </div>
                <div style="font-size:0.75rem; color:#6B7280; margin-top:4px;">
                    {req["requester"]} · {req["dept"]} · {req["time"]} · {render_badge(req["type"], "#4F46E5")} {render_priority_badge(req["urgency"])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">💬 Slack Intake Preview</div>', unsafe_allow_html=True)
        for msg in SLACK_CONVERSATION:
            is_bot = "Bot" in msg["user"]
            st.markdown(f"""
            <div class="slack-bubble">
                <span class="slack-user">{msg["avatar"]} {msg["user"]}</span>
                <span class="slack-time">{msg["time"]}</span>
                <div class="slack-msg">{msg["msg"]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">📧 Email Intake Preview</div>', unsafe_allow_html=True)
        email = EMAIL_INTAKE
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:1rem;">
            <div style="font-size:0.75rem; color:#6B7280;">From: <strong>{email["from_name"]}</strong> &lt;{email["from"]}&gt; · {email["dept"]}</div>
            <div style="font-size:0.95rem; font-weight:700; color:#1F2937; margin:0.5rem 0;">📧 {email["subject"]}</div>
            <div style="font-size:0.82rem; color:#374151; white-space:pre-line; line-height:1.6;">{email["body"]}</div>
            <hr style="border:none; border-top:1px solid #E5E7EB; margin:0.75rem 0;">
            <div style="font-size:0.78rem; font-weight:600; color:#4F46E5;">🤖 AI-Parsed Details</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.78rem; color:#374151; margin-top:0.4rem;">
                <div>Type: <strong>{email["parsed"]["matter_type"]}</strong></div>
                <div>Confidence: <strong>{email["parsed"]["confidence"]}</strong></div>
                <div>Urgency: <strong>{email["parsed"]["urgency"]}</strong></div>
                <div>Deal Value: <strong>{email["parsed"]["deal_value"]}</strong></div>
                <div>Counterparty: <strong>{email["parsed"]["counterparty"]}</strong></div>
                <div>Deadline: <strong>{email["parsed"]["deadline"]}</strong></div>
                <div>Assigned: <strong>{email["parsed"]["assigned_to"]}</strong></div>
                <div>Matter: <strong>{email["parsed"]["matter_id"]}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_footer()


# ════════════════════════════════════════════════════════════
# 2. MATTER MANAGEMENT
# ════════════════════════════════════════════════════════════
elif page == "📋 Matter Management":
    st.markdown("## 📋 Matter Management")

    view_mode = st.radio("View", ["Kanban Board", "List View", "Detail View"], horizontal=True)

    if view_mode == "Kanban Board":
        statuses = ["New", "In Review", "Pending Approval", "Approved", "Closed"]
        cols = st.columns(5)
        for idx, status in enumerate(statuses):
            with cols[idx]:
                status_color = STATUS_COLORS.get(status, "#6B7280")
                matters_in_status = [m for m in MATTERS if m["status"] == status]
                st.markdown(f"""
                <div style="background:{status_color}; color:white; padding:6px 12px; border-radius:8px 8px 0 0;
                            font-weight:700; font-size:0.8rem; text-align:center;">
                    {status} ({len(matters_in_status)})
                </div>
                """, unsafe_allow_html=True)
                for m in matters_in_status:
                    p_color = PRIORITY_COLORS.get(m["priority"], "#6B7280")
                    st.markdown(f"""
                    <div class="kanban-card">
                        <div class="card-id">{m["id"]}</div>
                        <div class="card-title">{m["title"]}</div>
                        <div>{render_badge(m["type"], "#4F46E5")} {render_badge(m["priority"], p_color)}</div>
                        <div class="card-meta">👤 {m["assignee"]["name"]}<br>📅 Due: {m["due"]}<br>📎 {m["documents"]} docs</div>
                    </div>
                    """, unsafe_allow_html=True)
                if not matters_in_status:
                    st.markdown('<div style="text-align:center; color:#9CA3AF; padding:1rem; font-size:0.8rem;">No matters</div>', unsafe_allow_html=True)

    elif view_mode == "List View":
        rows = []
        for m in MATTERS:
            rows.append({
                "ID": m["id"],
                "Title": m["title"],
                "Type": m["type"],
                "Status": m["status"],
                "Priority": m["priority"],
                "Assignee": m["assignee"]["name"],
                "Due": m["due"],
                "Docs": m["documents"],
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)

    elif view_mode == "Detail View":
        matter_options = {f'{m["id"]} — {m["title"]}': m for m in MATTERS}
        selected_key = st.selectbox("Select a matter", list(matter_options.keys()))
        m = matter_options[selected_key]

        st.markdown(f"### {m['title']}")
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            render_metric_card(m["id"], "Matter ID")
        with mc2:
            render_metric_card(m["type"], "Type", COLORS["primary"])
        with mc3:
            p_color = PRIORITY_COLORS.get(m["priority"], "#6B7280")
            render_metric_card(m["priority"], "Priority", p_color)
        with mc4:
            s_color = STATUS_COLORS.get(m["status"], "#6B7280")
            render_metric_card(m["status"], "Status", s_color)

        st.markdown("#### Summary")
        st.info(m["summary"])

        detail_col1, detail_col2 = st.columns(2)
        with detail_col1:
            st.markdown("#### Timeline")
            for event in m["timeline"]:
                st.markdown(f"""
                <div style="border-left:3px solid #4F46E5; padding:0.4rem 0.8rem; margin:0.3rem 0; font-size:0.82rem;">
                    <span style="color:#6B7280;">{event["time"]}</span> · <strong>{event["user"]}</strong><br>
                    {event["action"]}
                </div>
                """, unsafe_allow_html=True)

        with detail_col2:
            st.markdown("#### Tasks")
            for task in m["tasks"]:
                st.checkbox(task["task"], value=task["done"], key=f"task_{m['id']}_{task['task']}")

            st.markdown("#### Documents")
            st.markdown(f"📎 **{m['documents']}** document(s) linked to this matter.")

            st.markdown("#### Notes")
            notes = m.get("notes", "")
            st.text_area("Notes", value=notes if notes else "No notes yet.", height=100, key=f"notes_{m['id']}")

    render_footer()


# ════════════════════════════════════════════════════════════
# 3. AI ASSISTANT
# ════════════════════════════════════════════════════════════
elif page == "💬 AI Assistant":
    st.markdown("## 💬 AI Legal Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    main_col, side_col = st.columns([3, 2])

    with main_col:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and msg.get("citations"):
                    with st.expander("📚 Sources"):
                        for i, cite in enumerate(msg["citations"]):
                            st.markdown(f"**Source {i+1}:** {cite.get('document_id', 'Unknown')} — {cite.get('section', '')}")
                            st.caption(cite.get("chunk_text", ""))

        prompt = st.chat_input("Ask a legal question...")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = api_post("/search/ask", json_data={"query": prompt, "top_k": 5})

                if result and result.get("answer"):
                    answer = result["answer"]
                    citations = result.get("citations", [])
                    st.markdown(answer)
                    if citations:
                        with st.expander("📚 Sources"):
                            for i, cite in enumerate(citations):
                                st.markdown(f"**Source {i+1}:** {cite.get('document_id', 'Unknown')} — {cite.get('section', '')}")
                                st.caption(cite.get("chunk_text", ""))
                    st.session_state.chat_history.append({"role": "assistant", "content": answer, "citations": citations})
                else:
                    fallback = "I couldn't process that request. Please try rephrasing your question, or ensure documents have been uploaded to the knowledge base."
                    st.markdown(fallback)
                    st.session_state.chat_history.append({"role": "assistant", "content": fallback, "citations": []})

        st.markdown("""
        <div style="background:#FEF3C7; border:1px solid #F59E0B; border-radius:8px; padding:0.6rem 1rem; margin-top:1rem; font-size:0.8rem; color:#92400E;">
            ⚠️ AI responses are for guidance only. Always consult with your legal team for final decisions.
        </div>
        """, unsafe_allow_html=True)

    with side_col:
        if st.session_state.chat_history:
            st.markdown('<div class="section-header">Chat History</div>', unsafe_allow_html=True)
            user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
            for um in user_msgs[-5:]:
                st.markdown(f"• {um['content'][:60]}...")

        st.markdown('<div class="section-header">💬 Slack Bot Preview</div>', unsafe_allow_html=True)
        for msg in SLACK_CONVERSATION[:2]:
            st.markdown(f"""
            <div class="slack-bubble">
                <span class="slack-user">{msg["avatar"]} {msg["user"]}</span>
                <span class="slack-time">{msg["time"]}</span>
                <div class="slack-msg">{msg["msg"]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">📧 Email Bot Preview</div>', unsafe_allow_html=True)
        email = EMAIL_INTAKE
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:0.75rem; font-size:0.8rem;">
            <div><strong>From:</strong> {email["from_name"]}</div>
            <div><strong>Subject:</strong> {email["subject"]}</div>
            <div style="margin-top:0.3rem; color:#6B7280;">Auto-parsed → {email["parsed"]["matter_type"]} · {email["parsed"]["urgency"]}</div>
        </div>
        """, unsafe_allow_html=True)

    render_footer()


# ════════════════════════════════════════════════════════════
# 4. DOCUMENT INTELLIGENCE
# ════════════════════════════════════════════════════════════
elif page == "📄 Document Intelligence":
    st.markdown("## 📄 Document Intelligence")

    tab1, tab2, tab3 = st.tabs(["📤 Upload & Classify", "🔍 Clause Extraction", "🔄 Compare Contracts"])

    with tab1:
        up_col, lib_col = st.columns([1, 1])
        with up_col:
            st.markdown("#### Upload Document")
            uploaded_file = st.file_uploader("Choose a legal document", type=["pdf", "docx", "txt"], help="PDF, DOCX, or TXT")

            if uploaded_file and st.button("🚀 Upload & Classify", type="primary"):
                with st.spinner("Processing document..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    result = api_post("/documents/upload", files=files)

                if result:
                    st.success(f"✅ Uploaded: {result.get('filename', uploaded_file.name)}")
                    doc_id = result.get("document_id")

                    with st.spinner("🤖 Classifying..."):
                        cls_result = api_post(f"/analysis/classify/{doc_id}")

                    if cls_result and "classification" in cls_result:
                        cls = cls_result["classification"]
                        c1, c2 = st.columns(2)
                        with c1:
                            render_metric_card(cls.get("document_type", "Unknown"), "Document Type", COLORS["primary"])
                        with c2:
                            render_metric_card(f"{cls.get('confidence', 0):.0%}", "Confidence", COLORS["success"])
                        if cls.get("reasoning"):
                            st.info(f"💡 {cls['reasoning']}")
                        if cls.get("metadata"):
                            with st.expander("Extracted Metadata"):
                                st.json(cls["metadata"])

        with lib_col:
            st.markdown("#### Document Library")
            docs = get_documents()
            if docs:
                for doc in docs:
                    cls_data = json.loads(doc["classification"]) if doc.get("classification") else None
                    doc_type = cls_data.get("document_type", "Unclassified") if cls_data else "Unclassified"
                    with st.expander(f"📁 {doc['filename']} — {doc_type}"):
                        st.text(f"ID: {doc['document_id']}")
                        st.text(f"Type: {doc.get('file_type', '?')} | Pages: {doc.get('page_count', '?')}")
                        st.text(f"Status: {doc.get('status', 'unknown')}")
                        st.text(f"Uploaded: {doc.get('created_at', '')}")
            else:
                st.info("No documents uploaded yet.")

    with tab2:
        st.markdown("#### Clause Extraction & Risk Assessment")
        docs = get_documents()
        if not docs:
            st.warning("Upload a document first to extract clauses.")
        else:
            doc_options = {f"{d['filename']} ({d['document_id']})": d['document_id'] for d in docs}
            selected = st.selectbox("Select document", list(doc_options.keys()), key="extract_doc")
            doc_id = doc_options[selected]

            if st.button("🔍 Extract Clauses", type="primary"):
                with st.spinner("🤖 Analyzing clauses..."):
                    result = api_post(f"/analysis/extract/{doc_id}")

                if result and "extraction" in result:
                    extraction = result["extraction"]

                    st.markdown("##### Summary")
                    st.write(extraction.get("summary", ""))

                    meta = extraction.get("metadata", {})
                    risk_dist = meta.get("risk_distribution", {})
                    if risk_dist:
                        st.markdown("##### Risk Distribution")
                        rd_cols = st.columns(4)
                        risk_icons = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
                        risk_colors = {"LOW": COLORS["success"], "MEDIUM": COLORS["warning"], "HIGH": COLORS["orange"], "CRITICAL": COLORS["danger"]}
                        for i, (level, count) in enumerate(risk_dist.items()):
                            with rd_cols[i % 4]:
                                render_metric_card(f"{risk_icons.get(level, '')} {count}", level, risk_colors.get(level, "#6B7280"))

                    st.markdown("##### Extracted Clauses")
                    for clause in extraction.get("clauses", []):
                        risk = clause.get("risk_level", "LOW")
                        icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}.get(risk, "⚪")
                        with st.expander(f"{icon} {clause.get('clause_type', 'Unknown')} — {risk} risk"):
                            st.markdown(f"**Section:** {clause.get('section_reference', 'N/A')}")
                            st.markdown(f"**Text:** {clause.get('text', '')}")
                            st.markdown(f"**Risk Reason:** {clause.get('risk_reason', '')}")
                            if clause.get("playbook_note"):
                                st.info(f"📖 Playbook: {clause['playbook_note']}")

    with tab3:
        st.markdown("#### Compare Contracts")
        docs = get_documents()
        if len(docs) < 2:
            st.warning("Upload at least 2 documents to compare.")
        else:
            doc_options = {f"{d['filename']} ({d['document_id']})": d['document_id'] for d in docs}
            cmp1, cmp2 = st.columns(2)
            with cmp1:
                doc_a_key = st.selectbox("Original", list(doc_options.keys()), key="cmp_a")
            with cmp2:
                doc_b_key = st.selectbox("Revised", list(doc_options.keys()), key="cmp_b")

            if st.button("🔄 Compare", type="primary"):
                doc_a_id = doc_options[doc_a_key]
                doc_b_id = doc_options[doc_b_key]
                if doc_a_id == doc_b_id:
                    st.error("Select two different documents.")
                else:
                    with st.spinner("🤖 Comparing..."):
                        result = api_post("/analysis/compare", json_data={"doc_a_id": doc_a_id, "doc_b_id": doc_b_id})

                    if result and "comparison" in result:
                        comp = result["comparison"]
                        st.markdown("##### Summary")
                        st.write(comp.get("summary", ""))

                        if comp.get("new_risks"):
                            st.error("🚨 New Risks Identified")
                            for risk in comp["new_risks"]:
                                st.markdown(f"- {risk}")

                        if comp.get("recommendation"):
                            st.info(f"📋 {comp['recommendation']}")

                        for change in comp.get("changes", []):
                            icon = {"added": "🟢", "removed": "🔴", "modified": "🟡"}.get(change.get("type"), "⚪")
                            with st.expander(f"{icon} {change.get('clause', 'Unknown')} — {change.get('type', '')}"):
                                if change.get("original"):
                                    st.markdown(f"**Original:** {change['original']}")
                                if change.get("revised"):
                                    st.markdown(f"**Revised:** {change['revised']}")
                                st.markdown(f"**Risk Impact:** {change.get('risk_impact', 'N/A')}")

    render_footer()


# ════════════════════════════════════════════════════════════
# 5. DASHBOARD
# ════════════════════════════════════════════════════════════
elif page == "📊 Dashboard":
    st.markdown("## 📊 Executive Dashboard")

    d_col1, d_col2 = st.columns([3, 1])
    with d_col2:
        date_range = st.date_input("Date Range", value=(date.today() - timedelta(days=180), date.today()))

    open_matters = len([m for m in MATTERS if m["status"] not in ["Closed", "Approved"]])
    total_requests = sum(h["requests"] for h in HISTORICAL_DATA)
    avg_cycle = round(sum(h["avg_cycle_days"] for h in HISTORICAL_DATA) / len(HISTORICAL_DATA), 1)
    active_matters = len([m for m in MATTERS if m["status"] in ["In Review", "Pending Approval"]])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card(open_matters, "Total Open Matters", COLORS["primary"])
    with m2:
        render_metric_card(total_requests, "Requests (6 months)", COLORS["success"])
    with m3:
        render_metric_card(f"{avg_cycle}d", "Avg Cycle Time", COLORS["warning"])
    with m4:
        render_metric_card(active_matters, "Active Matters", COLORS["orange"])

    pending_long = [m for m in MATTERS if m["status"] == "Pending Approval"]
    if pending_long:
        st.warning(f"⚠️ **Bottleneck Alert:** {len(pending_long)} matter(s) are in 'Pending Approval' for >7 days and may need escalation.")

    st.markdown("")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_type = px.pie(
            names=list(MATTERS_BY_TYPE.keys()),
            values=list(MATTERS_BY_TYPE.values()),
            title="Matters by Type",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_type.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        st.plotly_chart(fig_type, use_container_width=True)

    with chart_col2:
        status_counts = {}
        for m in MATTERS:
            status_counts[m["status"]] = status_counts.get(m["status"], 0) + 1
        fig_status = px.bar(
            x=list(status_counts.keys()),
            y=list(status_counts.values()),
            title="Matters by Status",
            color=list(status_counts.keys()),
            color_discrete_map=STATUS_COLORS,
        )
        fig_status.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=350, showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        st.plotly_chart(fig_status, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        months = [h["month"] for h in HISTORICAL_DATA]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=months, y=[h["requests"] for h in HISTORICAL_DATA], name="Requests", line=dict(color=COLORS["primary"], width=3), mode="lines+markers"))
        fig_trend.add_trace(go.Scatter(x=months, y=[h["resolved"] for h in HISTORICAL_DATA], name="Resolved", line=dict(color=COLORS["success"], width=3), mode="lines+markers"))
        fig_trend.update_layout(title="Request Volume (6 Months)", margin=dict(t=40, b=20, l=20, r=20), height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        st.plotly_chart(fig_trend, use_container_width=True)

    with chart_col4:
        fig_workload = px.bar(
            x=list(WORKLOAD.values()),
            y=list(WORKLOAD.keys()),
            orientation="h",
            title="Workload by Assignee",
            color_discrete_sequence=[COLORS["primary"]],
        )
        fig_workload.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_workload, use_container_width=True)

    chart_col5, chart_col6 = st.columns(2)

    with chart_col5:
        fig_resp = px.bar(
            x=list(AVG_RESPONSE_BY_TYPE.keys()),
            y=list(AVG_RESPONSE_BY_TYPE.values()),
            title="Avg Response Time by Type (days)",
            color_discrete_sequence=[COLORS["warning"]],
        )
        fig_resp.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        st.plotly_chart(fig_resp, use_container_width=True)

    with chart_col6:
        risk_colors_map = {"LOW": COLORS["success"], "MEDIUM": COLORS["warning"], "HIGH": COLORS["orange"], "CRITICAL": COLORS["danger"]}
        fig_risk = px.pie(
            names=list(RISK_DISTRIBUTION.keys()),
            values=list(RISK_DISTRIBUTION.values()),
            title="Risk Distribution",
            color=list(RISK_DISTRIBUTION.keys()),
            color_discrete_map=risk_colors_map,
        )
        fig_risk.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12))
        st.plotly_chart(fig_risk, use_container_width=True)

    render_footer()


# ════════════════════════════════════════════════════════════
# 6. PRIVACY & SAFETY
# ════════════════════════════════════════════════════════════
elif page == "🔒 Privacy & Safety":
    st.markdown("## 🔒 Privacy & Safety Center")

    st.markdown('<div class="section-header">How Your Data Flows</div>', unsafe_allow_html=True)
    flow_cols = st.columns(5)
    flow_steps = [
        ("📥", "Document Upload", "Encrypted in transit (TLS 1.3)", True),
        ("🔒", "Processing", "Isolated compute, no data sharing", True),
        ("🧠", "AI Analysis", "Prompts sent to LLM — no training", True),
        ("📊", "Results Storage", "Encrypted at rest (AES-256)", True),
        ("🌐", "External Sharing", "Never shared without consent", False),
    ]
    for i, (icon, title, desc, safe) in enumerate(flow_steps):
        with flow_cols[i]:
            mark = "✅" if safe else "❌"
            bg = "#ECFDF5" if safe else "#FEF2F2"
            border_c = COLORS["success"] if safe else COLORS["danger"]
            st.markdown(f"""
            <div class="flow-step" style="background:{bg}; border-color:{border_c};">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:700; font-size:0.85rem; margin:0.3rem 0; color:#1F2937 !important;">{title}</div>
                <div style="font-size:0.75rem; color:#6B7280 !important;">{desc}</div>
                <div style="font-size:1.2rem; margin-top:0.3rem;">{mark}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Deployment Modes</div>', unsafe_allow_html=True)
    dep_col1, dep_col2 = st.columns(2)
    with dep_col1:
        st.markdown(f"""
        <div style="background:#EEF2FF; border:2px solid {COLORS["primary"]}; border-radius:12px; padding:1.25rem;">
            <div style="font-size:1.3rem;">🏢</div>
            <div style="font-weight:700; font-size:1rem; margin:0.3rem 0; color:#000000 !important;">Self-Hosted</div>
            <div style="font-size:0.82rem; color:#000000 !important; line-height:1.6;">
                • All data stays on your infrastructure<br>
                • LLM runs locally or via private endpoint<br>
                • Full audit control<br>
                • HIPAA / SOC 2 ready<br>
                • Air-gapped option available
            </div>
        </div>
        """, unsafe_allow_html=True)
    with dep_col2:
        st.markdown(f"""
        <div style="background:#F0FDF4; border:2px solid {COLORS["success"]}; border-radius:12px; padding:1.25rem;">
            <div style="font-size:1.3rem;">☁️</div>
            <div style="font-weight:700; font-size:1rem; margin:0.3rem 0; color:#000000 !important;">Hybrid Cloud</div>
            <div style="font-size:0.82rem; color:#000000 !important; line-height:1.6;">
                • Documents stored on your cloud<br>
                • AI processing via secure API<br>
                • Data encrypted in transit & at rest<br>
                • No data retention by AI provider<br>
                • Faster deployment, lower ops overhead
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">What the AI Sees</div>', unsafe_allow_html=True)
    transparency_steps = [
        ("1️⃣", "Document Chunking", "Your document is split into small, context-aware chunks. No full document is sent to the LLM."),
        ("2️⃣", "Prompt Construction", "Only relevant chunks + your query are assembled into a prompt. PII is redacted when possible."),
        ("3️⃣", "LLM Processing", "The prompt is sent to the AI model. No data is stored or used for training."),
        ("4️⃣", "Response Filtering", "AI output is validated, citations are verified, and confidence scores are calculated."),
        ("5️⃣", "Audit Logging", "Every interaction is logged with timestamp, user, action, and input/output summaries."),
    ]
    for icon, title, desc in transparency_steps:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:0.6rem 1rem; margin:0.3rem 0; display:flex; align-items:center; gap:0.75rem;">
            <div style="font-size:1.3rem; min-width:2rem;">{icon}</div>
            <div>
                <div style="font-weight:600; font-size:0.85rem; color:#000000 !important;">{title}</div>
                <div style="font-size:0.78rem; color:#000000 !important;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Integrations & Security</div>', unsafe_allow_html=True)
    int_cols = st.columns(4)
    for i, integ in enumerate(INTEGRATIONS):
        with int_cols[i % 4]:
            connected = integ["connected"]
            border_c = COLORS["success"] if connected else COLORS["border"]
            status_text = "Connected" if connected else "Not Connected"
            status_color = COLORS["success"] if connected else COLORS["text_muted"]
            st.markdown(f"""
            <div class="integration-card" style="border-color:{border_c}; margin-bottom:0.75rem;">
                <div style="font-size:1.5rem;">{integ["icon"]}</div>
                <div style="font-weight:700; font-size:0.9rem; margin:0.3rem 0; color:#1F2937 !important;">{integ["name"]}</div>
                <div style="font-size:0.75rem; color:#6B7280 !important;">{integ["desc"]}</div>
                <div style="font-size:0.72rem; font-weight:600; color:{status_color}; margin-top:0.4rem;">● {status_text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Audit & Compliance</div>', unsafe_allow_html=True)
    audit_result = api_get("/governance/audit/report")
    if audit_result:
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            render_metric_card(audit_result.get("total_operations", 0), "Total Operations", COLORS["primary"])
        with ac2:
            render_metric_card(f"{audit_result.get('average_latency_ms', 0)}ms", "Avg Latency")
        with ac3:
            render_metric_card(len(audit_result.get("action_breakdown", {})), "Actions Tracked", COLORS["success"])

        breakdown = audit_result.get("action_breakdown", {})
        if breakdown:
            for action, count in breakdown.items():
                max_val = max(breakdown.values()) if breakdown.values() else 1
                st.progress(count / max_val, text=f"{action}: {count}")

        logs = audit_result.get("logs", [])
        if logs:
            st.dataframe(logs, use_container_width=True, hide_index=True)

        st.download_button("📥 Export Audit Report", data=json.dumps(audit_result, indent=2, default=str), file_name="legallens_audit_report.json", mime="application/json")
    else:
        st.info("No audit data available yet. Start using LegalLens to generate audit logs.")

    st.markdown('<div class="section-header">Model Selection Guide</div>', unsafe_allow_html=True)
    model_data = [
        {"Model": "Claude 3.5 Sonnet", "Provider": "Anthropic", "Context": "200K tokens", "Best For": "Contract analysis, clause extraction", "Privacy": "No training on data", "Cost": "$$"},
        {"Model": "GPT-4o", "Provider": "OpenAI", "Context": "128K tokens", "Best For": "General legal Q&A", "Privacy": "Enterprise API — no training", "Cost": "$$$"},
        {"Model": "Llama 3.1 70B", "Provider": "Meta (Self-hosted)", "Context": "128K tokens", "Best For": "Air-gapped deployments", "Privacy": "Fully local — max privacy", "Cost": "$"},
        {"Model": "Mistral Large", "Provider": "Mistral AI", "Context": "32K tokens", "Best For": "Multi-language contracts", "Privacy": "EU-hosted option", "Cost": "$$"},
    ]
    st.dataframe(model_data, use_container_width=True, hide_index=True)

    render_footer()
