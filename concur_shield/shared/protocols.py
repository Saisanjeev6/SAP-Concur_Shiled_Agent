"""
ConcurShield AI — Inter-Agent Communication Protocol
Structured message passing, event logging, and state management
for true multi-agent orchestration.
"""

import json
from datetime import datetime
from typing import Any, Optional


# ================================
# AGENT MESSAGE PROTOCOL
# ================================

def create_agent_message(
    sender: str,
    receiver: str,
    message_type: str,
    payload: dict,
    reasoning: str = "",
) -> dict:
    """Create a structured inter-agent message."""
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "sender": sender,
        "receiver": receiver,
        "message_type": message_type,  # HANDOFF, DATA, ALERT, DECISION
        "payload": payload,
        "reasoning": reasoning,
    }


# ================================
# STATE KEYS — shared "whiteboard"
# ================================

# Each agent reads from upstream and writes to its own key
STATE_KEYS = {
    "pipeline_status": "pipeline_status",          # Pipeline metadata
    "agent_log": "agent_log",                      # Ordered event log
    "messages": "messages",                        # Inter-agent messages

    # Agent output keys (written via output_key)
    "expense_generator": "expense_generator_output",
    "receipt_intelligence": "receipt_intelligence_output",
    "policy_compliance": "policy_compliance_output",
    "fraud_detection": "fraud_detection_output",
    "audit_escalation": "audit_escalation_output",
}


# ================================
# AGENT LIFECYCLE CALLBACKS
# ================================

def _get_or_init_log(state: dict) -> list:
    """Get or initialize the agent event log."""
    if "agent_log" not in state:
        state["agent_log"] = []
    log = state["agent_log"]
    return log if isinstance(log, list) else []


def _get_or_init_messages(state: dict) -> list:
    """Get or initialize the messages list."""
    if "messages" not in state:
        state["messages"] = []
    msgs = state["messages"]
    return msgs if isinstance(msgs, list) else []


def before_agent_callback(callback_context):
    """
    Lifecycle hook: runs BEFORE each agent starts processing.
    Logs reasoning steps and reads upstream messages.
    """
    agent_name = callback_context.agent_name
    state = callback_context.state

    # Initialize pipeline status on first agent
    if "pipeline_status" not in state:
        state["pipeline_status"] = {
            "started_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "current_agent": agent_name,
            "agents_completed": [],
            "agents_remaining": [],
        }

    # Update current agent
    pipeline = state.get("pipeline_status", {})
    if isinstance(pipeline, dict):
        pipeline["current_agent"] = agent_name
        state["pipeline_status"] = pipeline

    # Log agent entry
    log = _get_or_init_log(state)
    log.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "event": "AGENT_START",
        "agent": agent_name,
        "message": f"🚀 [{agent_name}] Starting processing...",
        "upstream_data_available": _list_available_state(state),
    })
    state["agent_log"] = log

    # Return None to let the agent proceed normally
    return None


def after_agent_callback(callback_context):
    """
    Lifecycle hook: runs AFTER each agent completes processing.
    Logs completion and sends handoff message to next agent.
    """
    agent_name = callback_context.agent_name
    state = callback_context.state

    # Determine next agent in pipeline
    agent_order = [
        "expense_generator",
        "receipt_intelligence",
        "policy_compliance",
        "fraud_detection",
        "audit_escalation",
    ]

    current_idx = -1
    for i, name in enumerate(agent_order):
        if name in agent_name:
            current_idx = i
            break

    next_agent = agent_order[current_idx + 1] if current_idx >= 0 and current_idx < len(agent_order) - 1 else "PIPELINE_COMPLETE"

    # Log agent completion
    log = _get_or_init_log(state)

    # Determine what this agent produced
    output_key = STATE_KEYS.get(agent_name.replace("_agent", ""), "")
    data_produced = "output_key: " + output_key if output_key else "conversation context"

    log.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "event": "AGENT_COMPLETE",
        "agent": agent_name,
        "message": f"✅ [{agent_name}] Completed. Handing off to → {next_agent}",
        "data_produced": data_produced,
    })
    state["agent_log"] = log

    # Create handoff message to next agent
    messages = _get_or_init_messages(state)
    handoff_msg = create_agent_message(
        sender=agent_name,
        receiver=next_agent,
        message_type="HANDOFF",
        payload={
            "status": "completed",
            "output_location": f"state['{output_key}']" if output_key else "conversation",
        },
        reasoning=f"Agent {agent_name} has completed its analysis. Data is available for {next_agent} to consume.",
    )
    messages.append(handoff_msg)
    state["messages"] = messages

    # Update pipeline status
    pipeline = state.get("pipeline_status", {})
    if isinstance(pipeline, dict):
        completed = pipeline.get("agents_completed", [])
        if isinstance(completed, list):
            completed.append(agent_name)
        pipeline["agents_completed"] = completed
        pipeline["current_agent"] = next_agent
        if next_agent == "PIPELINE_COMPLETE":
            pipeline["completed_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        state["pipeline_status"] = pipeline

    return None


def _list_available_state(state: dict) -> list:
    """List what state keys have data from upstream agents."""
    available = []
    for key_name, state_key in STATE_KEYS.items():
        if state_key in state and state.get(state_key):
            available.append(state_key)
    return available
