"""
ConcurShield AI — Root Orchestrator Agent
Multi-agent expense intelligence pipeline with true inter-agent communication.

Architecture:
    User Request → Root Orchestrator → SequentialAgent Pipeline:
        1. Expense Generator    → writes to state["expense_generator_output"]
        2. Receipt Intelligence → reads ↑, writes to state["receipt_intelligence_output"]
        3. Policy Compliance    → reads ↑↑, writes to state["policy_compliance_output"]
        4. Fraud Detection      → reads ↑↑↑, writes to state["fraud_detection_output"]
        5. Audit & Escalation   → reads ALL ↑, writes to state["audit_escalation_output"]

    Each agent:
    - Has before/after lifecycle callbacks for event logging
    - Passes structured handoff messages to the next agent
    - Logs reasoning steps for audit trail
    - Writes output to a dedicated state key via output_key
"""

from google.adk import Agent
from google.adk.agents import SequentialAgent

# Import sub-agents (each pre-configured with callbacks + output_key)
from concur_shield.agents.expense_generator.agent import expense_generator_agent
from concur_shield.agents.receipt_intelligence.agent import receipt_intelligence_agent
from concur_shield.agents.policy_compliance.agent import policy_compliance_agent
from concur_shield.agents.fraud_detection.agent import fraud_detection_agent
from concur_shield.agents.audit_escalation.agent import audit_escalation_agent

# Import pipeline-level callbacks
from concur_shield.shared.protocols import before_agent_callback, after_agent_callback


# ============================================================
# Sequential Pipeline — orchestrates all 5 agents in sequence
# Each agent reads from upstream state + writes to its own key
# ============================================================

expense_pipeline = SequentialAgent(
    name="expense_intelligence_pipeline",
    description="Orchestrates 5 agents in sequence: Expense Generator → Receipt Intelligence → Policy Compliance → Fraud Detection → Audit & Escalation. Each agent communicates via shared session state and structured handoff messages.",
    sub_agents=[
        expense_generator_agent,      # Writes → expense_generator_output
        receipt_intelligence_agent,    # Reads ↑ → Writes receipt_intelligence_output
        policy_compliance_agent,       # Reads ↑↑ → Writes policy_compliance_output
        fraud_detection_agent,         # Reads ↑↑↑ → Writes fraud_detection_output
        audit_escalation_agent,        # Reads ALL → Writes audit_escalation_output
    ],
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)


# ============================================================
# Root Orchestrator — the entry point for ConcurShield AI
# ============================================================

root_agent = Agent(
    name="concur_shield_ai",
    model="gemini-2.5-flash",
    instruction="""You are **ConcurShield AI** — a Multi-Agent Expense Intelligence Simulator.
Built for hackathon demonstration using Google ADK, Vertex AI, and Antigravity.

🔰 SYSTEM OVERVIEW:
You orchestrate a pipeline of 5 specialized AI agents that COMMUNICATE with each other,
passing structured data through shared session state and handoff messages.

🏗️ YOUR AGENT TEAM (Sequential Pipeline):
```
Agent 1: 🟢 Expense Generator    → Creates profiles + expenses → state["expense_generator_output"]
    ↓ (handoff message + structured data)
Agent 2: 🟡 Receipt Intelligence  → Parses + classifies        → state["receipt_intelligence_output"]
    ↓ (handoff message + structured data)
Agent 3: 🔴 Policy Compliance     → Validates against rules     → state["policy_compliance_output"]
    ↓ (handoff message + structured data)
Agent 4: 🟠 Fraud Detection       → Computes risk score         → state["fraud_detection_output"]
    ↓ (handoff message + structured data)
Agent 5: 🔵 Audit & Escalation    → Final decision + report     → state["audit_escalation_output"]
```

📡 INTER-AGENT COMMUNICATION:
- Each agent writes its output to a dedicated state key (via output_key)
- Each agent reads upstream agents' output from state
- Structured handoff messages are passed between agents
- Before/after lifecycle callbacks log every agent's entry and exit
- Complete reasoning trail is maintained in state["agent_log"]

🎯 WHAT YOU CAN DO:
When the user asks you to process expenses, ALWAYS delegate to `expense_intelligence_pipeline`.

Example user requests:
- "Generate a synthetic expense report" → Full pipeline run
- "Create expenses with fraud patterns" → Pipeline with anomaly injection
- "Process a US sales executive's travel expenses" → Region-specific scenario
- "Run a high-risk fraud simulation" → Stress test with anomalies

💡 GREETING:
When the user says hello, introduce yourself as ConcurShield AI and explain:
1. You're a multi-agent system with 5 specialized agents
2. Agents communicate via structured messages and shared state
3. Each agent logs its reasoning for full auditability
4. The pipeline produces a comprehensive audit report

⚠️ IMPORTANT:
- Always delegate expense processing to the pipeline
- The pipeline handles all inter-agent communication automatically
- Final output includes the complete audit report + agent communication log
""",
    sub_agents=[expense_pipeline],
)
