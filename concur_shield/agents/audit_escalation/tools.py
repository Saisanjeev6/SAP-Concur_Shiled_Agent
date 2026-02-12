"""
Agent 5: Audit & Escalation Tools
Final authority — consolidates all findings and makes audit decisions.
"""

from typing import List
from concur_shield.shared.utils import generate_report_id, current_timestamp


def consolidate_findings(
    employee_id: str,
    employee_name: str,
    total_expenses: int,
    total_amount: float,
    currency: str,
    policy_approved: int,
    policy_rejected: int,
    policy_violations: List[str],
    fraud_risk_score: int,
    fraud_risk_level: str,
    fraud_signals: List[str],
    policy_needs_review: int = 0,
) -> dict:
    """
    Consolidates all findings from Policy Compliance and Fraud Detection into a unified view.

    Args:
        employee_id: Employee ID.
        employee_name: Employee name.
        total_expenses: Total number of expense items.
        total_amount: Total expense amount.
        currency: Currency code.
        policy_approved: Number of items approved by policy check.
        policy_needs_review: Deprecated in binary mode; retained for compatibility.
        policy_rejected: Number of items rejected.
        policy_violations: List of violation descriptions.
        fraud_risk_score: Fraud risk score (0-100).
        fraud_risk_level: Fraud risk level (LOW/MEDIUM/HIGH/CRITICAL).
        fraud_signals: List of fraud signal descriptions.

    Returns:
        Consolidated findings summary.
    """
    total_issues = policy_rejected + len(fraud_signals)

    # Calculate compliance rate
    compliance_rate = round(
        (policy_approved / total_expenses * 100) if total_expenses > 0 else 0, 1
    )

    return {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "report_summary": {
            "total_expenses": total_expenses,
            "total_amount": total_amount,
            "currency": currency,
        },
        "policy_summary": {
            "approved": policy_approved,
            "rejected": policy_rejected,
            "compliance_rate": f"{compliance_rate}%",
            "violations": policy_violations,
        },
        "fraud_summary": {
            "risk_score": fraud_risk_score,
            "risk_level": fraud_risk_level,
            "signals": fraud_signals,
            "signal_count": len(fraud_signals),
        },
        "total_issues": total_issues,
        "overall_health": "CLEAN" if total_issues == 0 else (
            "CONCERNING" if total_issues <= 2 else "CRITICAL"
        ),
    }


def make_audit_decision(
    employee_id: str,
    total_amount: float,
    total_expenses: int,
    policy_rejected: int,
    fraud_risk_score: int,
    fraud_risk_level: str,
    total_violations: int,
    total_fraud_signals: int,
    policy_needs_review: int = 0,
) -> dict:
    """
    Makes the final audit decision based on consolidated findings.

    Args:
        employee_id: Employee ID.
        total_amount: Total expense amount.
        total_expenses: Number of expense items.
        policy_rejected: Number of policy-rejected items.
        policy_needs_review: Deprecated in binary mode; retained for compatibility.
        fraud_risk_score: Fraud risk score (0-100).
        fraud_risk_level: Fraud risk level.
        total_violations: Total number of policy violations.
        total_fraud_signals: Total number of fraud signals.

    Returns:
        Audit decision with action items.
    """
    action_items = []

    # Binary decision logic.
    if fraud_risk_score >= 50 or policy_rejected >= 1 or total_fraud_signals >= 2:
        decision = "REJECTED"
        action_items.extend([
            "❌ Rejected due to risk/policy violations",
            "🔒 Payment suspended",
            "📧 Notification sent to employee and manager",
        ])
    else:
        decision = "APPROVED"
        action_items.extend([
            "✅ Approved — no significant issues detected",
            "💰 Process reimbursement immediately",
            "📁 Archive for audit trail",
        ])

    return {
        "employee_id": employee_id,
        "report_id": generate_report_id(),
        "decision": decision,
        "total_amount": total_amount,
        "total_items": total_expenses,
        "policy_violations": total_violations,
        "fraud_risk_score": fraud_risk_score,
        "fraud_signals_count": total_fraud_signals,
        "action_items": action_items,
        "processed_at": current_timestamp(),
    }


def generate_audit_report(
    employee_id: str,
    employee_name: str,
    department: str,
    region: str,
    report_id: str,
    decision: str,
    total_amount: float,
    currency: str,
    total_items: int,
    compliance_rate: str,
    fraud_risk_score: int,
    fraud_risk_level: str,
    policy_violations: List[str],
    fraud_signals: List[str],
    action_items: List[str],
) -> dict:
    """
    Generates a comprehensive audit report with all findings and decisions.

    Args:
        employee_id: Employee ID.
        employee_name: Employee name.
        department: Employee department.
        region: Employee region.
        report_id: Audit report ID.
        decision: Final decision (APPROVED/REJECTED).
        total_amount: Total expense amount.
        currency: Currency code.
        total_items: Number of expense items.
        compliance_rate: Policy compliance rate (e.g., "80.0%").
        fraud_risk_score: Fraud risk score (0-100).
        fraud_risk_level: Fraud risk level.
        policy_violations: List of violation descriptions.
        fraud_signals: List of fraud signal descriptions.
        action_items: List of action items.

    Returns:
        Complete audit report as structured JSON.
    """
    # Decision emoji
    decision_indicator = {
        "APPROVED": "✅ APPROVED",
        "REJECTED": "❌ REJECTED",
    }

    return {
        "audit_report": {
            "header": {
                "report_id": report_id,
                "system": "ConcurShield AI v1.0",
                "generated_at": current_timestamp(),
                "decision": decision_indicator.get(decision, decision),
            },
            "employee": {
                "id": employee_id,
                "name": employee_name,
                "department": department,
                "region": region,
            },
            "financial_summary": {
                "total_amount": f"{currency} {total_amount}",
                "total_items": total_items,
                "compliance_rate": compliance_rate,
            },
            "risk_assessment": {
                "fraud_risk_score": f"{fraud_risk_score}/100",
                "fraud_risk_level": fraud_risk_level,
                "fraud_signals": fraud_signals if fraud_signals else ["None detected"],
            },
            "policy_compliance": {
                "violations": policy_violations if policy_violations else ["No violations"],
                "violation_count": len(policy_violations),
            },
            "decision_details": {
                "final_decision": decision,
                "action_items": action_items,
            },
        }
    }
