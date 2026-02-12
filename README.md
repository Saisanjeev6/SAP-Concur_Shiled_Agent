# 🛡️ ConcurShield AI

### Multi-Agent Expense Intelligence Simulator

> Built with **Google ADK** · **Vertex AI (Gemini 2.5 Flash)** · **Antigravity**

---

## 🎯 Problem Statement

Enterprise expense fraud detection and policy enforcement require massive volumes of realistic transaction data — but:

| Challenge | Impact |
|-----------|--------|
| Real employee data can't be reused | Privacy & compliance risk |
| Fraud scenarios are rare in production | ML models lack edge-case training data |
| Policy engines aren't continuously tested | Inconsistent enforcement |
| Approval workflows aren't stress-tested | Fraud slips through |

**Result**: Testing environments are weak. Fraud slips through. Policies are inconsistently enforced.

---

## 💡 Solution

A **multi-agent AI system** where 5 specialized agents **communicate with each other** through structured messages and shared state to:

✅ Generate realistic synthetic expense scenarios  
✅ Parse and classify receipts with NLP  
✅ Validate policy compliance across regions  
✅ Detect fraud patterns and compute risk scores  
✅ Make automated audit decisions  

**All without using real employee data.**

---

## 🏗️ System Architecture

### Orchestration Flow

```
                    ┌──────────────────────┐
                    │    👤 User Request    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   🔰 Root Orchestrator│
                    │   (concur_shield_ai)  │
                    └──────────┬───────────┘
                               │ delegates to
                    ┌──────────▼───────────────────────────────────┐
                    │      SequentialAgent Pipeline                 │
                    │                                               │
                    │  ┌─────────────────────────────────────────┐  │
                    │  │ 🟢 Agent 1: Expense Generator           │  │
                    │  │    Tools: generate_employee_profile      │  │
                    │  │           generate_expense_report        │  │
                    │  │           inject_anomaly                 │  │
                    │  │    Writes → state["expense_generator_output"]
                    │  └──────────────┬──────────────────────────┘  │
                    │       HANDOFF ──┤── structured message         │
                    │  ┌──────────────▼──────────────────────────┐  │
                    │  │ 🟡 Agent 2: Receipt Intelligence        │  │
                    │  │    Tools: parse_receipt                  │  │
                    │  │           enrich_receipt_metadata        │  │
                    │  │    Reads ↑  Writes → state["receipt_intelligence_output"]
                    │  └──────────────┬──────────────────────────┘  │
                    │       HANDOFF ──┤── structured message         │
                    │  ┌──────────────▼──────────────────────────┐  │
                    │  │ 🔴 Agent 3: Policy Compliance           │  │
                    │  │    Tools: get_expense_policy             │  │
                    │  │           validate_expense               │  │
                    │  │    Reads ↑↑ Writes → state["policy_compliance_output"]
                    │  └──────────────┬──────────────────────────┘  │
                    │       HANDOFF ──┤── structured message         │
                    │  ┌──────────────▼──────────────────────────┐  │
                    │  │ 🟠 Agent 4: Fraud Detection             │  │
                    │  │    Tools: detect_duplicate_claims        │  │
                    │  │           analyze_submission_velocity    │  │
                    │  │           check_vendor_patterns          │  │
                    │  │           compute_risk_score             │  │
                    │  │    Reads ↑↑↑ Writes → state["fraud_detection_output"]
                    │  └──────────────┬──────────────────────────┘  │
                    │       HANDOFF ──┤── structured message         │
                    │  ┌──────────────▼──────────────────────────┐  │
                    │  │ 🔵 Agent 5: Audit & Escalation          │  │
                    │  │    Tools: consolidate_findings           │  │
                    │  │           make_audit_decision            │  │
                    │  │           generate_audit_report          │  │
                    │  │    Reads ALL Writes → state["audit_escalation_output"]
                    │  └─────────────────────────────────────────┘  │
                    └──────────────────────┬───────────────────────┘
                                           │
                    ┌──────────────────────▼───────────────────────┐
                    │  📋 Final Audit Report                       │
                    │  Decision: AUTO_APPROVED / MANUAL_REVIEW /   │
                    │            ESCALATED                          │
                    └──────────────────────────────────────────────┘
```

### Inter-Agent Communication Protocol

This is **not** just sequential API calls. Agents genuinely communicate:

```
┌─────────────────┐    structured     ┌─────────────────┐
│   Agent N        │───── message ────▶│   Agent N+1      │
│                  │    (HANDOFF)      │                  │
│  output_key ─────┼──▶ state[key] ───┼─▶ reads state   │
│  after_callback ─┼──▶ agent_log  ───┼─▶ before_callback│
│  reasoning log   │    messages[]    │  reasoning log   │
└─────────────────┘                   └─────────────────┘
```

| Mechanism | Description |
|-----------|------------|
| `output_key` | Each agent writes final output to `session.state["<agent>_output"]` |
| `state["messages"]` | Structured HANDOFF messages with sender, receiver, payload, reasoning |
| `state["agent_log"]` | Timestamped event log: AGENT_START → AGENT_COMPLETE for every agent |
| `state["pipeline_status"]` | Tracks current agent, completed list, start/end timestamps |
| `before_agent_callback` | Logs agent entry, lists available upstream data |
| `after_agent_callback` | Logs completion, creates handoff message to next agent |

---

## 🤖 Agent Descriptions

### Agent 1: 🟢 Synthetic Expense Generator

**Purpose**: The data engine. Creates the raw material for the entire pipeline.

| Tool | Function |
|------|----------|
| `generate_employee_profile()` | Creates realistic employees with name, department, grade, region, risk tier |
| `generate_expense_report()` | Produces 1-10 expense line items: flights, hotels, meals, taxis, per diem |
| `inject_anomaly()` | Injects specific fraud patterns: `duplicate`, `inflated`, `split_expense`, `weekend_claim` |

**Data Pools**: 16 employee names, 20 cities (global), 10 departments, 40+ vendors across 7 categories.

---

### Agent 2: 🟡 Receipt Intelligence

**Purpose**: NLP-powered receipt parsing. Transforms raw expenses into structured, classified data.

| Tool | Function |
|------|----------|
| `parse_receipt()` | Classifies vendor into 9 categories, assigns merchant codes (MCC), computes confidence score |
| `enrich_receipt_metadata()` | Adds risk flags: `WEEKEND_TRANSACTION`, `HIGH_VALUE`, `NON_BUSINESS_CATEGORY`, `INTERNATIONAL` |

**Vendor Classification**: Keyword-based NLP matching across 50+ vendor patterns.

---

### Agent 3: 🔴 Policy Compliance

**Purpose**: Enterprise rule enforcer. Validates against region-specific corporate policies.

| Tool | Function |
|------|----------|
| `get_expense_policy()` | Returns full policy for region: limits, rules, restrictions |
| `validate_expense()` | Multi-rule validation engine with 5 compliance checks |

**Supported Regions** (5):

| Region | Meal Limit | Hotel Limit | Currency | Weekend | Entertainment |
|--------|-----------|-------------|----------|---------|---------------|
| 🇺🇸 US | $75 | $350 | USD | ❌ | ❌ |
| 🇩🇪 DE | €60 | €250 | EUR | ❌ | ❌ |
| 🇮🇳 IN | ₹3,500 | ₹12,000 | INR | ❌ | ❌ |
| 🇬🇧 UK | £60 | £280 | GBP | ❌ | ❌ |
| 🇸🇬 SG | S$100 | S$450 | SGD | ❌ | ❌ |

**Validation Rules**: Amount limits · Weekend claims · Category restrictions · Suspicious vendor keywords · Receipt thresholds

**Outcomes**: `APPROVED` (0 violations) · `NEEDS_REVIEW` (1 violation) · `REJECTED` (2+ violations)

---

### Agent 4: 🟠 Fraud Detection

**Purpose**: Security intelligence. Multi-signal fraud pattern analysis with risk scoring.

| Tool | Function |
|------|----------|
| `detect_duplicate_claims()` | Finds duplicate receipt numbers or identical amount+vendor+date combinations |
| `analyze_submission_velocity()` | Flags rapid-fire submissions (4+ expenses/day) or batch fabrication patterns |
| `check_vendor_patterns()` | Identifies repeated vendors, non-business vendor names, potential kickbacks |
| `compute_risk_score()` | Weighted aggregation of all signals into a 0-100 risk score |

---

### Agent 5: 🔵 Audit & Escalation

**Purpose**: Final authority. Consolidates all upstream findings and makes the audit decision.

| Tool | Function |
|------|----------|
| `consolidate_findings()` | Merges policy violations + fraud signals into unified view with compliance rate |
| `make_audit_decision()` | Tiered decision engine with specific action items per tier |
| `generate_audit_report()` | Produces professional structured audit report |

**Decisions**: `AUTO_APPROVED` · `MANUAL_REVIEW` · `ESCALATED`

---

## 📊 Risk Scoring Logic

### Signal Weights

```
Risk Score = Σ(weighted signals), capped at 100

┌──────────────────────────┬────────┬───────────┐
│ Signal                   │ Weight │ Max Score  │
├──────────────────────────┼────────┼───────────┤
│ Duplicate Claims         │ ×20    │ 40        │
│ Policy Violations        │ ×10    │ 25        │
│ Suspicious Vendors       │ ×8     │ 15        │
│ Velocity Anomalies       │ ×5     │ 10        │
│ Weekend Claims           │ ×5     │ 10        │
│ High Total Amount (>$5K) │ +5     │ 5         │
│ Very High Amount (>$10K) │ +5     │ 5         │
└──────────────────────────┴────────┴───────────┘
                            Maximum │ 100       │
```

### Risk Levels & Actions

| Score | Level | Visual | Decision | Action |
|-------|-------|--------|----------|--------|
| 0–24 | 🟢 LOW | ██░░░ | AUTO_APPROVED | Process reimbursement, archive |
| 25–49 | 🟡 MEDIUM | ███░░ | MANUAL_REVIEW | Route to manager, request docs |
| 50–74 | 🟠 HIGH | ████░ | MANUAL_REVIEW | Finance team review, hold payment |
| 75–100 | 🔴 CRITICAL | █████ | ESCALATED | Compliance Officer, suspend payment, investigate |

### Example Scenarios

| Scenario | Expected Score | Decision |
|----------|---------------|----------|
| Clean report, 5 items, all within limits | 0 | ✅ AUTO_APPROVED |
| 1 inflated meal + 1 weekend claim | 15 | ✅ AUTO_APPROVED |
| 2 duplicate receipts + 1 policy violation | 50 | ⚠️ MANUAL_REVIEW |
| 3 duplicates + suspicious vendor + 2 violations | 86 | 🚨 ESCALATED |

---

## 🔧 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent Framework** | Google ADK 1.25 | Multi-agent orchestration, SequentialAgent pipeline |
| **LLM** | Gemini 2.5 Flash (via Vertex AI) | Agent reasoning, tool selection, natural language |
| **Communication** | ADK Session State + output_key | Inter-agent structured data passing |
| **Lifecycle** | before/after_agent_callback | Event logging, handoff messages, pipeline tracking |
| **Language** | Python 3.13 | All agent logic and tools |
| **Data Models** | TypedDict (PEP 589) | 7 shared schemas for type-safe agent communication |
| **Collaboration** | Antigravity | Agent development and pair programming |

---

## 📁 Project Structure

```
concur_shield/
├── __init__.py                          # Package init, re-exports root_agent
├── agent.py                             # Root Orchestrator + SequentialAgent Pipeline
│
├── shared/
│   ├── schemas.py                       # 7 TypedDict data models (shared contracts)
│   ├── utils.py                         # ID generators, date helpers, 6 data pools
│   └── protocols.py                     # Inter-agent protocol, callbacks, messages
│
└── agents/
    ├── expense_generator/               # Agent 1: Synthetic data engine
    │   ├── agent.py                     #   LLM Agent (output_key + callbacks)
    │   └── tools.py                     #   3 tools (profile, report, anomaly)
    │
    ├── receipt_intelligence/            # Agent 2: NLP receipt parsing
    │   ├── agent.py                     #   LLM Agent (output_key + callbacks)
    │   └── tools.py                     #   2 tools (parse, enrich)
    │
    ├── policy_compliance/               # Agent 3: Rule enforcement
    │   ├── agent.py                     #   LLM Agent (output_key + callbacks)
    │   └── tools.py                     #   2 tools (policy, validate)
    │
    ├── fraud_detection/                 # Agent 4: Risk scoring
    │   ├── agent.py                     #   LLM Agent (output_key + callbacks)
    │   └── tools.py                     #   4 tools (duplicates, velocity, vendor, score)
    │
    └── audit_escalation/                # Agent 5: Final authority
        ├── agent.py                     #   LLM Agent (output_key + callbacks)
        └── tools.py                     #   3 tools (consolidate, decide, report)
```

**Total**: 5 agents · 14 tools · 7 shared schemas · 1 communication protocol

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Google Cloud Project with Vertex AI API enabled
- `pip3 install google-adk`

### Setup

```bash
# Clone & configure
git clone <repo-url>
cd Synthetic-Data-Fabricator-Agent
cp .env.example .env
```

**Option A — Vertex AI (recommended)**:
```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

**Option B — Google AI Studio**:
```env
GOOGLE_API_KEY=your-api-key
```

### Run

```bash
# Interactive CLI
adk run concur_shield

# Web UI (recommended for demo)
adk web concur_shield
```

### Sample Prompts

| Prompt | Pipeline Behavior |
|--------|-------------------|
| "Generate a synthetic expense report for a US Sales exec" | Clean scenario → likely AUTO_APPROVED |
| "Create expenses with fraudulent entries" | Anomaly injection → higher risk score |
| "Process expenses for a consultant in Germany with weekend claims" | DE policy + violations |
| "Run a high-risk fraud simulation with duplicates" | Stress test → likely ESCALATED |
| "Generate 10 expense items for an Indian employee" | INR currency + IN policy limits |

---

## 🔮 Future Scalability

### Near-Term Enhancements

| Feature | Description |
|---------|------------|
| **ParallelAgent** | Run Policy Compliance + Fraud Detection in parallel (both read from Agent 2) |
| **Human-in-the-Loop** | Pause pipeline at MANUAL_REVIEW for human approval before continuing |
| **Persistent State** | Use `DatabaseSessionService` for audit trail across sessions |
| **Memory Service** | Enable agents to recall patterns from past expense reports |

### Platform Integration

| Integration | How |
|-------------|-----|
| **SAP Concur API** | Replace synthetic generator with real Concur expense data ingestion |
| **SAP S/4HANA** | Push audit decisions back to SAP for automated workflow |
| **Google Cloud Storage** | Store audit reports and receipt images in GCS |
| **BigQuery** | Log all pipeline telemetry for analytics dashboards |
| **Pub/Sub** | Event-driven pipeline triggers on new expense submissions |

### ML & Intelligence

| Feature | Approach |
|---------|---------|
| **Adaptive Risk Scoring** | Fine-tune Gemini on historical fraud data for better signal weights |
| **Anomaly Detection ML** | Train supervised model on synthetic + real edge cases |
| **Receipt OCR** | Integrate Google Vision AI for actual receipt image processing |
| **Behavioral Profiling** | Build per-employee spending baselines for deviation detection |
| **Cross-Report Analysis** | Detect fraud patterns across multiple reports over time |

### Enterprise Scale

| Capability | Technology |
|------------|-----------|
| **Multi-tenant** | ADK `app:` state prefix for org-level policies |
| **Real-time Processing** | Cloud Run + Pub/Sub for event-driven pipeline |
| **Global Policy Engine** | Expand to 50+ regions with localized rules |
| **Audit Compliance** | SOX/SOC2 audit trail via immutable Cloud Logging |
| **Dashboard** | Looker/Data Studio for fraud analytics visualization |

---

## 👥 Team

Built by a team of 5 for the hackathon.

**Tech Stack**: Google ADK · Vertex AI (Gemini 2.5 Flash) · Python 3.13 · Antigravity