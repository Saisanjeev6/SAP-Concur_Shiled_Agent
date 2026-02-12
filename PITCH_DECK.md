# 🛡️ ConcurShield AI

## Multi-Agent Expense Intelligence Simulator

---

## 🏢 The Problem

> Expense fraud costs enterprises **$2.8 billion annually** globally.
> Yet testing environments remain dangerously weak.

| Pain Point | Business Impact |
|------------|----------------|
| Real expense data can't be reused | Privacy laws block realistic testing |
| Fraud scenarios are rare in production | ML models lack edge-case training data |
| Policy engines aren't stress-tested | Inconsistent enforcement across regions |
| Approval workflows aren't battle-tested | Fraudulent claims slip through |

**Bottom line**: Companies can't test what they can't simulate.

---

## 💡 Our Solution

**ConcurShield AI** — a multi-agent AI system that simulates the entire expense lifecycle:

```
Generate → Parse → Validate → Detect → Decide
```

5 specialized AI agents that **talk to each other**, pass structured data,
and produce enterprise-grade audit decisions — all on synthetic data.

**Zero real employee data. Full fraud coverage. Continuous testing.**

---

## 🏗️ Architecture — True Multi-Agent Orchestration

```
   👤 User
    │
    ▼
┌─────────────────────────────────────────────┐
│          🔰 Root Orchestrator               │
│          (Google ADK + Gemini 2.5 Flash)     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│       SequentialAgent Pipeline               │
│                                              │
│  🟢 Expense Generator ──── HANDOFF ────┐     │
│     ↳ profiles + expenses + anomalies  │     │
│                                        ▼     │
│  🟡 Receipt Intelligence ── HANDOFF ────┐    │
│     ↳ vendor classification + flags    │     │
│                                        ▼     │
│  🔴 Policy Compliance ───── HANDOFF ────┐    │
│     ↳ 5-region rule validation         │     │
│                                        ▼     │
│  🟠 Fraud Detection ─────── HANDOFF ────┐    │
│     ↳ risk score 0-100                 │     │
│                                        ▼     │
│  🔵 Audit & Escalation                       │
│     ↳ AUTO_APPROVED / MANUAL_REVIEW /        │
│       ESCALATED                              │
└──────────────────────────────────────────────┘
```

**Not just sequential API calls** — agents communicate via:
- 📦 Shared session state (`output_key` chaining)
- 📨 Structured handoff messages (sender → receiver + payload)
- 📋 Event logging (timestamped agent lifecycle)
- 🧠 Reasoning trails (WHY each decision was made)

---

## 🤖 The 5 Agents

| # | Agent | What It Does | Tools |
|---|-------|-------------|-------|
| 1 | 🟢 **Expense Generator** | Creates realistic employee profiles + diverse expense items. Injects fraud anomalies. | 3 |
| 2 | 🟡 **Receipt Intelligence** | NLP parsing — classifies vendors into 9 categories. Adds merchant codes. Flags risks. | 2 |
| 3 | 🔴 **Policy Compliance** | Validates against region-specific policies (US, DE, IN, UK, SG). 5 compliance rules. | 2 |
| 4 | 🟠 **Fraud Detection** | Detects duplicates, velocity anomalies, vendor patterns. Computes 0-100 risk score. | 4 |
| 5 | 🔵 **Audit & Escalation** | Consolidates everything. Makes final decision. Generates professional audit report. | 3 |

**14 total tools** across 5 agents. **7 shared data schemas**. **1 communication protocol**.

---

## 📊 Risk Scoring Engine

### Weighted Signal Aggregation

| Signal | Weight | Max |
|--------|--------|-----|
| Duplicate Claims | ×20 | 40 |
| Policy Violations | ×10 | 25 |
| Suspicious Vendors | ×8 | 15 |
| Velocity Anomalies | ×5 | 10 |
| Weekend Claims | ×5 | 10 |

### Decision Tiers

| Score | Level | Action |
|-------|-------|--------|
| 0-24 | 🟢 LOW | ✅ Auto-approved |
| 25-49 | 🟡 MEDIUM | 👤 Route to manager |
| 50-74 | 🟠 HIGH | 🏦 Finance review, hold payment |
| 75-100 | 🔴 CRITICAL | 🚨 Compliance escalation |

---

## 🎬 Live Demo Flow

```
Prompt: "Generate expenses for a US Sales exec with some fraudulent entries"

Agent 1 → Employee: Sarah Chen (EMP-A3F2), 6 expenses, $3,247.50
          Injected: 1 duplicate receipt, 1 inflated meal

Agent 2 → Parsed 7 receipts (6 original + 1 duplicate)
          Classified: 2 Airline, 2 Restaurant, 1 Hotel, 1 Transport, 1 Other
          Flagged: 1 HIGH_VALUE, 1 WEEKEND

Agent 3 → Policy validation: 4 APPROVED, 2 NEEDS_REVIEW, 1 REJECTED
          Violation: $187.50 meal exceeds $75 limit
          Compliance rate: 57.1%

Agent 4 → Risk Score: 52/100 (HIGH)
          Signals: 1 duplicate receipt, 1 amount inflation, 1 policy violation

Agent 5 → Decision: ⚠️ MANUAL REVIEW
          Action: Route to Finance, hold payment, request docs
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | **Google ADK 1.25** |
| LLM | **Gemini 2.5 Flash** (Vertex AI) |
| Communication | Session State + output_key + callbacks |
| Language | Python 3.13 |
| Data Models | TypedDict (7 schemas) |
| Collaboration | Antigravity |

---

## 🏆 Hackathon Judging Criteria Alignment

| Criteria | How We Score |
|----------|-------------|
| **Innovation** | Multi-agent fraud simulation — not just rules, but AI reasoning |
| **Technical Merit** | 5 agents, 14 tools, structured communication protocol, lifecycle callbacks |
| **Use of Google ADK** | SequentialAgent, output_key, before/after callbacks, session state |
| **Use of Vertex AI** | Gemini 2.5 Flash powering all agent reasoning |
| **Business Impact** | Solves real enterprise problem — SAP Concur-scale expense fraud |
| **Demo Quality** | ADK Web UI shows live agent-to-agent flow |

---

## 🔮 Future Vision

| Phase | Feature |
|-------|---------|
| **Next** | ParallelAgent for Policy + Fraud in parallel |
| **Soon** | SAP Concur API integration for real data |
| **Later** | BigQuery analytics dashboard, ML-trained risk models |
| **Enterprise** | Multi-tenant, SOX/SOC2 audit trail, 50+ region policies |

---

## 👥 Team

**Team of 5** · Google ADK Hackathon

*Protecting enterprises from expense fraud — one synthetic report at a time.*

---

> **ConcurShield AI** — Because the best defense is a synthetic offense. 🛡️
