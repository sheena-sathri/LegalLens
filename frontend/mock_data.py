"""Mock data for LegalLens Legal AI Hub — realistic demo data for all modules."""

import random
from datetime import datetime, timedelta

ASSIGNEES = [
    {"name": "Sarah Chen", "role": "Senior Contracts Attorney", "team": "Contracts"},
    {"name": "James Rodriguez", "role": "Associate General Counsel", "team": "Commercial"},
    {"name": "Lisa Park", "role": "IP Counsel", "team": "IP & Patents"},
    {"name": "Michael Torres", "role": "Compliance Manager", "team": "Compliance"},
    {"name": "Emily Watson", "role": "Employment Counsel", "team": "Employment"},
]

REQUESTERS = [
    {"name": "Alex Kim", "dept": "Engineering", "email": "alex.kim@company.com"},
    {"name": "Priya Sharma", "dept": "Sales", "email": "priya.sharma@company.com"},
    {"name": "David Chen", "dept": "Product", "email": "david.chen@company.com"},
    {"name": "Rachel Green", "dept": "Marketing", "email": "rachel.green@company.com"},
    {"name": "Tom Baker", "dept": "Finance", "email": "tom.baker@company.com"},
    {"name": "Nina Patel", "dept": "HR", "email": "nina.patel@company.com"},
    {"name": "Chris Lee", "dept": "Engineering", "email": "chris.lee@company.com"},
    {"name": "Maria Santos", "dept": "Sales", "email": "maria.santos@company.com"},
    {"name": "Jordan Hayes", "dept": "Product", "email": "jordan.hayes@company.com"},
    {"name": "Sam Wilson", "dept": "Operations", "email": "sam.wilson@company.com"},
]

MATTER_TYPES = [
    "NDA Review", "MSA Review", "Employment Agreement", "Vendor Onboarding",
    "IP Assignment", "Policy Update", "Compliance Audit", "Data Processing Agreement",
    "Contract Amendment", "Licensing Agreement",
]

def _date(days_ago):
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")

def _date_obj(days_ago):
    return datetime.now() - timedelta(days=days_ago)

MATTERS = [
    {
        "id": "M-2024-0142",
        "title": "Vendor NDA — TechFlow Solutions",
        "type": "NDA Review",
        "status": "New",
        "priority": "High",
        "requester": REQUESTERS[0],
        "assignee": ASSIGNEES[0],
        "created": _date(1),
        "due": _date(-5),
        "documents": 1,
        "summary": "Standard mutual NDA for new data analytics vendor. Requester needs expedited review for Q1 onboarding deadline.",
        "timeline": [
            {"time": _date(1), "action": "Created via Slack intake", "user": "System"},
            {"time": _date(1), "action": "Auto-classified as NDA Review (confidence: 94%)", "user": "AI"},
            {"time": _date(0.5), "action": "Assigned to Sarah Chen, Contracts Team", "user": "System"},
        ],
        "tasks": [
            {"task": "Review confidentiality scope", "done": False},
            {"task": "Check term and termination provisions", "done": False},
            {"task": "Verify carve-outs for pre-existing IP", "done": False},
        ],
        "notes": "",
    },
    {
        "id": "M-2024-0141",
        "title": "Cloud Services MSA — DataVault Inc",
        "type": "MSA Review",
        "status": "New",
        "priority": "Urgent",
        "requester": REQUESTERS[1],
        "assignee": ASSIGNEES[1],
        "created": _date(2),
        "due": _date(-3),
        "documents": 3,
        "summary": "Enterprise cloud infrastructure MSA with $2.4M annual commitment. Multiple risk flags on liability and data handling.",
        "timeline": [
            {"time": _date(2), "action": "Created via email intake from priya.sharma@company.com", "user": "System"},
            {"time": _date(2), "action": "Auto-classified as MSA Review (confidence: 91%)", "user": "AI"},
            {"time": _date(1.8), "action": "Priority escalated to Urgent — deal value >$1M", "user": "System"},
            {"time": _date(1.5), "action": "Assigned to James Rodriguez, Commercial Team", "user": "System"},
        ],
        "tasks": [
            {"task": "Review liability cap provisions", "done": False},
            {"task": "Assess data processing terms", "done": False},
            {"task": "Check SLA commitments", "done": False},
            {"task": "Review termination for convenience clause", "done": False},
        ],
        "notes": "Counterparty is pushing for unlimited liability on data breaches. Need to negotiate.",
    },
    {
        "id": "M-2024-0140",
        "title": "Engineering Contractor Agreement — DevStudio",
        "type": "Employment Agreement",
        "status": "New",
        "priority": "Medium",
        "requester": REQUESTERS[6],
        "assignee": ASSIGNEES[4],
        "created": _date(3),
        "due": _date(-7),
        "documents": 2,
        "summary": "Independent contractor agreement for specialized ML engineering team. 6-month engagement with IP assignment provisions.",
        "timeline": [
            {"time": _date(3), "action": "Submitted via self-service portal", "user": REQUESTERS[6]["name"]},
            {"time": _date(3), "action": "Auto-classified as Employment Agreement (confidence: 87%)", "user": "AI"},
            {"time": _date(2.5), "action": "Assigned to Emily Watson, Employment Team", "user": "System"},
        ],
        "tasks": [
            {"task": "Verify contractor vs employee classification", "done": False},
            {"task": "Review IP assignment clauses", "done": False},
            {"task": "Check non-compete provisions", "done": False},
        ],
        "notes": "",
    },
    {
        "id": "M-2024-0138",
        "title": "SaaS Vendor Onboarding — Analytix Pro",
        "type": "Vendor Onboarding",
        "status": "In Review",
        "priority": "Medium",
        "requester": REQUESTERS[3],
        "assignee": ASSIGNEES[0],
        "created": _date(5),
        "due": _date(-2),
        "documents": 4,
        "summary": "New marketing analytics platform vendor. Requires DPA review, security questionnaire, and standard vendor agreement.",
        "timeline": [
            {"time": _date(5), "action": "Created via email intake", "user": "System"},
            {"time": _date(5), "action": "Auto-classified as Vendor Onboarding (confidence: 89%)", "user": "AI"},
            {"time": _date(4.5), "action": "Assigned to Sarah Chen, Contracts Team", "user": "System"},
            {"time": _date(4), "action": "Document uploaded: analytix_msa_v1.pdf", "user": REQUESTERS[3]["name"]},
            {"time": _date(3.5), "action": "AI clause extraction complete — 1 HIGH risk flag", "user": "AI"},
            {"time": _date(3), "action": "Comment: Reviewing data handling provisions", "user": "Sarah Chen"},
        ],
        "tasks": [
            {"task": "Complete vendor security assessment", "done": True},
            {"task": "Review DPA terms", "done": True},
            {"task": "Negotiate liability provisions", "done": False},
            {"task": "Get procurement sign-off", "done": False},
        ],
        "notes": "Vendor has agreed to our standard DPA template. Liability cap still being negotiated.",
    },
    {
        "id": "M-2024-0136",
        "title": "Patent License Agreement — InnovateTech",
        "type": "IP Assignment",
        "status": "In Review",
        "priority": "High",
        "requester": REQUESTERS[2],
        "assignee": ASSIGNEES[2],
        "created": _date(8),
        "due": _date(-1),
        "documents": 2,
        "summary": "Inbound patent license for core ML technology. Critical for product roadmap. Complex royalty structure needs review.",
        "timeline": [
            {"time": _date(8), "action": "Created via Slack intake", "user": "System"},
            {"time": _date(8), "action": "Auto-classified as IP Assignment (confidence: 82%)", "user": "AI"},
            {"time": _date(7.5), "action": "Assigned to Lisa Park, IP & Patents Team", "user": "System"},
            {"time": _date(7), "action": "Document uploaded: patent_license_draft.pdf", "user": REQUESTERS[2]["name"]},
            {"time": _date(6), "action": "AI clause extraction complete — 3 HIGH risk flags", "user": "AI"},
            {"time": _date(5), "action": "Comment: Royalty calculation needs restructuring", "user": "Lisa Park"},
            {"time": _date(3), "action": "Revised terms shared with counterparty", "user": "Lisa Park"},
        ],
        "tasks": [
            {"task": "Review grant scope and field of use", "done": True},
            {"task": "Analyze royalty structure", "done": True},
            {"task": "Check sublicensing rights", "done": False},
            {"task": "Confirm patent validity representations", "done": False},
        ],
        "notes": "Counterparty open to restructuring royalties from per-unit to flat fee. Lisa recommending flat fee at $450K/yr.",
    },
    {
        "id": "M-2024-0133",
        "title": "GDPR Data Processing Agreement — EuroCloud",
        "type": "Data Processing Agreement",
        "status": "Pending Approval",
        "priority": "High",
        "requester": REQUESTERS[4],
        "assignee": ASSIGNEES[3],
        "created": _date(12),
        "due": _date(-1),
        "documents": 3,
        "summary": "DPA for EU data processing with cloud infrastructure provider. Requires GDPR Article 28 compliance review.",
        "timeline": [
            {"time": _date(12), "action": "Created via self-service portal", "user": REQUESTERS[4]["name"]},
            {"time": _date(12), "action": "Auto-classified as Data Processing Agreement (confidence: 96%)", "user": "AI"},
            {"time": _date(11), "action": "Assigned to Michael Torres, Compliance Team", "user": "System"},
            {"time": _date(10), "action": "Document uploaded: eurocloud_dpa_v2.pdf", "user": REQUESTERS[4]["name"]},
            {"time": _date(9), "action": "AI clause extraction complete — 2 MEDIUM risk flags", "user": "AI"},
            {"time": _date(7), "action": "Negotiation round 1 complete", "user": "Michael Torres"},
            {"time": _date(4), "action": "Final terms agreed — pending VP Legal approval", "user": "Michael Torres"},
        ],
        "tasks": [
            {"task": "GDPR Article 28 compliance check", "done": True},
            {"task": "Review sub-processor list", "done": True},
            {"task": "Verify data transfer mechanisms", "done": True},
            {"task": "Get VP Legal sign-off", "done": False},
        ],
        "notes": "All substantive terms agreed. Waiting on VP Legal approval. Standard Clauses (SCCs) included for cross-border transfers.",
    },
    {
        "id": "M-2024-0131",
        "title": "Annual Compliance Audit — SOC 2 Type II",
        "type": "Compliance Audit",
        "status": "Pending Approval",
        "priority": "Medium",
        "requester": REQUESTERS[9],
        "assignee": ASSIGNEES[3],
        "created": _date(15),
        "due": _date(2),
        "documents": 5,
        "summary": "Annual SOC 2 Type II audit preparation. Coordinating with external auditors and internal teams.",
        "timeline": [
            {"time": _date(15), "action": "Created by Compliance Team", "user": "Michael Torres"},
            {"time": _date(14), "action": "Audit scope defined", "user": "Michael Torres"},
            {"time": _date(12), "action": "Evidence collection started", "user": "Michael Torres"},
            {"time": _date(8), "action": "Draft report received from auditors", "user": "System"},
            {"time": _date(5), "action": "Internal review of findings complete", "user": "Michael Torres"},
            {"time": _date(2), "action": "Remediation plan submitted — pending approval", "user": "Michael Torres"},
        ],
        "tasks": [
            {"task": "Collect access control evidence", "done": True},
            {"task": "Review change management logs", "done": True},
            {"task": "Validate encryption standards", "done": True},
            {"task": "Address auditor findings", "done": True},
            {"task": "Final report approval", "done": False},
        ],
        "notes": "Two minor findings related to access review cadence. Remediation plan addresses both.",
    },
    {
        "id": "M-2024-0128",
        "title": "Enterprise License Agreement — GlobalSoft",
        "type": "Licensing Agreement",
        "status": "Approved",
        "priority": "High",
        "requester": REQUESTERS[7],
        "assignee": ASSIGNEES[1],
        "created": _date(20),
        "due": _date(5),
        "documents": 4,
        "summary": "3-year enterprise software license with $1.8M TCV. Fully negotiated and approved.",
        "timeline": [
            {"time": _date(20), "action": "Created via Slack intake", "user": "System"},
            {"time": _date(20), "action": "Auto-classified as Licensing Agreement (confidence: 93%)", "user": "AI"},
            {"time": _date(19), "action": "Assigned to James Rodriguez, Commercial Team", "user": "System"},
            {"time": _date(18), "action": "Initial review complete — 4 risk flags", "user": "AI"},
            {"time": _date(15), "action": "Negotiation round 1", "user": "James Rodriguez"},
            {"time": _date(10), "action": "Negotiation round 2 — key terms agreed", "user": "James Rodriguez"},
            {"time": _date(5), "action": "VP Legal approved", "user": "VP Legal"},
            {"time": _date(3), "action": "Sent to counterparty for signature", "user": "James Rodriguez"},
        ],
        "tasks": [
            {"task": "Review license scope", "done": True},
            {"task": "Negotiate usage limits", "done": True},
            {"task": "Review auto-renewal terms", "done": True},
            {"task": "Get VP approval", "done": True},
            {"task": "Counterparty signature", "done": False},
        ],
        "notes": "Approved. Awaiting counterparty execution. Expected within 5 business days.",
    },
    {
        "id": "M-2024-0125",
        "title": "HR Policy Update — Remote Work Guidelines",
        "type": "Policy Update",
        "status": "Approved",
        "priority": "Low",
        "requester": REQUESTERS[5],
        "assignee": ASSIGNEES[4],
        "created": _date(25),
        "due": _date(7),
        "documents": 2,
        "summary": "Updated remote work policy incorporating hybrid work model. Approved and ready for company-wide distribution.",
        "timeline": [
            {"time": _date(25), "action": "Submitted via self-service portal", "user": REQUESTERS[5]["name"]},
            {"time": _date(25), "action": "Auto-classified as Policy Update (confidence: 90%)", "user": "AI"},
            {"time": _date(24), "action": "Assigned to Emily Watson, Employment Team", "user": "System"},
            {"time": _date(20), "action": "Draft reviewed with HR leadership", "user": "Emily Watson"},
            {"time": _date(15), "action": "Revised based on feedback", "user": "Emily Watson"},
            {"time": _date(10), "action": "Final approval from CHRO", "user": "CHRO"},
        ],
        "tasks": [
            {"task": "Draft policy updates", "done": True},
            {"task": "HR leadership review", "done": True},
            {"task": "Legal compliance check", "done": True},
            {"task": "CHRO approval", "done": True},
            {"task": "Distribute to employees", "done": True},
        ],
        "notes": "Policy effective March 1, 2024. Communications team has been briefed.",
    },
    {
        "id": "M-2024-0120",
        "title": "Settlement Agreement — Contractor Dispute",
        "type": "Employment Agreement",
        "status": "Closed",
        "priority": "Urgent",
        "requester": REQUESTERS[5],
        "assignee": ASSIGNEES[4],
        "created": _date(35),
        "due": _date(20),
        "documents": 6,
        "summary": "Resolved contractor payment dispute. Settlement reached at $45K with mutual release. Fully executed and closed.",
        "timeline": [
            {"time": _date(35), "action": "Escalated by HR — contractor dispute", "user": REQUESTERS[5]["name"]},
            {"time": _date(35), "action": "Auto-classified as Employment Agreement (confidence: 78%)", "user": "AI"},
            {"time": _date(34), "action": "Assigned to Emily Watson — priority escalated to Urgent", "user": "System"},
            {"time": _date(30), "action": "Initial assessment complete", "user": "Emily Watson"},
            {"time": _date(25), "action": "Mediation session scheduled", "user": "Emily Watson"},
            {"time": _date(22), "action": "Settlement terms agreed — $45K", "user": "Emily Watson"},
            {"time": _date(21), "action": "Settlement agreement drafted", "user": "Emily Watson"},
            {"time": _date(20), "action": "Fully executed — matter closed", "user": "Emily Watson"},
        ],
        "tasks": [
            {"task": "Initial fact-finding", "done": True},
            {"task": "Risk assessment", "done": True},
            {"task": "Mediation preparation", "done": True},
            {"task": "Draft settlement agreement", "done": True},
            {"task": "Execute and close", "done": True},
        ],
        "notes": "Matter closed. Settlement paid. Mutual release executed. No further action needed.",
    },
]

def get_historical_data():
    months = []
    now = datetime.now()
    data = []
    for i in range(6):
        month = now - timedelta(days=30 * (5 - i))
        month_label = month.strftime("%b %Y")
        base = 18 + i * 4 + random.randint(-2, 2)
        data.append({
            "month": month_label,
            "requests": base,
            "resolved": base - random.randint(1, 4),
            "avg_cycle_days": round(5.5 - i * 0.3 + random.uniform(-0.5, 0.5), 1),
        })
    return data

HISTORICAL_DATA = get_historical_data()

MATTERS_BY_TYPE = {
    "NDA Review": 14,
    "Contract Review": 10,
    "Policy Question": 8,
    "Compliance Check": 4,
    "Employment": 5,
    "IP Review": 3,
    "Vendor Onboarding": 6,
    "Other": 4,
}

RISK_DISTRIBUTION = {"LOW": 42, "MEDIUM": 28, "HIGH": 18, "CRITICAL": 7}

WORKLOAD = {
    "Sarah Chen": 12,
    "James Rodriguez": 8,
    "Lisa Park": 6,
    "Michael Torres": 10,
    "Emily Watson": 9,
}

AVG_RESPONSE_BY_TYPE = {
    "NDA Review": 2.1,
    "MSA Review": 4.8,
    "Employment": 3.2,
    "Compliance": 5.1,
    "IP Review": 6.3,
    "Policy Update": 1.8,
    "Vendor Onboarding": 3.9,
}

RECENT_REQUESTS = [
    {"time": _date(0.1), "request": "Need NDA reviewed for new data vendor", "requester": "Alex Kim", "dept": "Engineering", "status": "New", "type": "NDA Review", "urgency": "High"},
    {"time": _date(0.3), "request": "What's our policy on software license compliance?", "requester": "David Chen", "dept": "Product", "status": "Triaged", "type": "Policy Question", "urgency": "Low"},
    {"time": _date(0.5), "request": "Contract amendment needed for GlobalSoft renewal", "requester": "Maria Santos", "dept": "Sales", "status": "In Progress", "type": "Contract Amendment", "urgency": "Medium"},
    {"time": _date(0.8), "request": "IP assignment for contractor deliverables", "requester": "Chris Lee", "dept": "Engineering", "status": "Triaged", "type": "IP Assignment", "urgency": "Medium"},
    {"time": _date(1.2), "request": "Urgent: Customer requesting DPA before deal closes Friday", "requester": "Priya Sharma", "dept": "Sales", "status": "In Progress", "type": "Data Processing Agreement", "urgency": "Urgent"},
    {"time": _date(1.5), "request": "Need employment agreement template for new hire", "requester": "Nina Patel", "dept": "HR", "status": "Resolved", "type": "Employment Agreement", "urgency": "Low"},
    {"time": _date(2.0), "request": "Annual vendor compliance review kickoff", "requester": "Sam Wilson", "dept": "Operations", "status": "In Progress", "type": "Compliance Audit", "urgency": "Medium"},
]

INTEGRATIONS = [
    {"name": "Slack", "icon": "💬", "desc": "Intake requests and chatbot via Slack channels and DMs", "connected": True},
    {"name": "Email", "icon": "📧", "desc": "Auto-parse incoming legal requests from email", "connected": True},
    {"name": "Ironclad", "icon": "📝", "desc": "CLM sync — push/pull contracts and metadata", "connected": False},
    {"name": "iManage", "icon": "📁", "desc": "Document management system integration", "connected": False},
    {"name": "DocuSign", "icon": "✍️", "desc": "E-signature workflow for approved contracts", "connected": True},
    {"name": "Salesforce", "icon": "☁️", "desc": "Matter tracking linked to customer accounts", "connected": False},
    {"name": "Jira", "icon": "📋", "desc": "Task management for legal project workflows", "connected": True},
    {"name": "SSO (Okta/Azure AD)", "icon": "🔐", "desc": "Single sign-on and identity management", "connected": True},
]

SLACK_CONVERSATION = [
    {"user": "Jordan Hayes", "avatar": "👤", "msg": "#legal I need an NDA for TechFlow Solutions — new vendor for the data team", "time": "10:23 AM"},
    {"user": "LegalLens Bot", "avatar": "🤖", "msg": "Got it! I've created matter **#M-2024-0142**.\n\n📋 **Classified as:** NDA Review (94% confidence)\n👤 **Assigned to:** Sarah Chen, Contracts Team\n⏱️ **ETA:** 2 business days\n🔗 Track status: [View Matter →](#)\n\nI'll notify you when it's ready for review!", "time": "10:23 AM"},
    {"user": "Jordan Hayes", "avatar": "👤", "msg": "Perfect, thanks! Can you also check if we have a standard NDA template?", "time": "10:24 AM"},
    {"user": "LegalLens Bot", "avatar": "🤖", "msg": "Yes! We have 3 approved NDA templates:\n1. **Mutual NDA** — Standard (most common)\n2. **One-way NDA** — Receiving party only\n3. **Mutual NDA** — Enhanced (for IP-heavy deals)\n\nI've attached the Standard Mutual NDA to matter #M-2024-0142. Sarah will customize it for TechFlow.", "time": "10:24 AM"},
]

EMAIL_INTAKE = {
    "from": "priya.sharma@company.com",
    "from_name": "Priya Sharma",
    "dept": "Sales",
    "subject": "URGENT: Need contract reviewed before Friday close",
    "body": "Hi Legal Team,\n\nWe're closing a $2.4M cloud infrastructure deal with DataVault Inc this Friday. I've attached the MSA they sent over — can someone review ASAP?\n\nKey concerns:\n- Their liability cap seems low\n- Data handling terms need review\n- Auto-renewal clause\n\nPlease prioritize, the customer is waiting.\n\nThanks,\nPriya",
    "parsed": {
        "matter_type": "MSA Review",
        "confidence": "91%",
        "urgency": "Urgent",
        "deal_value": "$2.4M",
        "counterparty": "DataVault Inc",
        "deadline": "Friday",
        "attachments": ["datavault_msa_v1.pdf"],
        "assigned_to": "James Rodriguez",
        "matter_id": "M-2024-0141",
    },
}
