"""
Agent 4: Fraud Detection Tools
Pattern-based fraud signal detection and risk scoring.
"""

import random
from typing import List
from collections import Counter


def detect_duplicate_claims(
    expense_ids: List[str],
    receipt_numbers: List[str],
    amounts: List[float],
    vendors: List[str],
    dates: List[str],
) -> dict:
    """
    Detects duplicate expense claims by analyzing receipt numbers, amounts, and vendor patterns.

    Args:
        expense_ids: List of expense IDs to analyze.
        receipt_numbers: Corresponding receipt numbers.
        amounts: Corresponding expense amounts.
        vendors: Corresponding vendor names.
        dates: Corresponding expense dates.

    Returns:
        Detection results with duplicate pairs and severity.
    """
    duplicates = []

    # Check for duplicate receipt numbers
    receipt_counts = Counter(receipt_numbers)
    for receipt, count in receipt_counts.items():
        if count > 1:
            indices = [i for i, r in enumerate(receipt_numbers) if r == receipt]
            affected_ids = [expense_ids[i] for i in indices]
            duplicates.append({
                "signal_type": "duplicate_receipt",
                "severity": "HIGH",
                "description": f"Receipt {receipt} appears {count} times across expenses",
                "affected_expense_ids": affected_ids,
                "confidence": 0.95,
            })

    # Check for same-amount same-vendor same-day
    for i in range(len(expense_ids)):
        for j in range(i + 1, len(expense_ids)):
            if (amounts[i] == amounts[j] and
                vendors[i] == vendors[j] and
                dates[i] == dates[j] and
                expense_ids[i] != expense_ids[j]):
                duplicates.append({
                    "signal_type": "duplicate_claim",
                    "severity": "CRITICAL",
                    "description": f"Identical amount ${amounts[i]} at {vendors[i]} on {dates[i]}",
                    "affected_expense_ids": [expense_ids[i], expense_ids[j]],
                    "confidence": 0.92,
                })

    return {
        "check": "duplicate_claims",
        "duplicates_found": len(duplicates),
        "signals": duplicates,
    }


def analyze_submission_velocity(
    employee_id: str,
    expense_dates: List[str],
    expense_ids: List[str],
) -> dict:
    """
    Analyzes the velocity of expense submissions to detect rapid-fire or bulk submissions.

    Args:
        employee_id: The employee being analyzed.
        expense_dates: List of expense dates.
        expense_ids: Corresponding expense IDs.

    Returns:
        Velocity analysis with flags for unusual submission patterns.
    """
    signals = []

    if not expense_dates:
        return {"check": "submission_velocity", "signals": [], "velocity_flag": False}

    # Count expenses per day
    date_counts = Counter(expense_dates)
    for date, count in date_counts.items():
        if count >= 4:
            signals.append({
                "signal_type": "velocity_anomaly",
                "severity": "MEDIUM",
                "description": f"Employee {employee_id} submitted {count} expenses on {date} — unusually high volume",
                "affected_expense_ids": [
                    expense_ids[i] for i, d in enumerate(expense_dates) if d == date
                ],
                "confidence": 0.78,
            })

    # Check for too many unique dates (scattered submissions)
    unique_dates = len(set(expense_dates))
    total = len(expense_dates)
    if total > 5 and unique_dates <= 2:
        signals.append({
            "signal_type": "velocity_anomaly",
            "severity": "LOW",
            "description": f"All {total} expenses concentrated in only {unique_dates} days — potential batch fabrication",
            "affected_expense_ids": expense_ids,
            "confidence": 0.65,
        })

    return {
        "check": "submission_velocity",
        "signals": signals,
        "velocity_flag": len(signals) > 0,
    }


def check_vendor_patterns(
    vendors: List[str],
    amounts: List[float],
    expense_ids: List[str],
) -> dict:
    """
    Identifies suspicious vendor patterns such as repeated vendors or unusual naming.

    Args:
        vendors: List of vendor names.
        amounts: Corresponding amounts.
        expense_ids: Corresponding expense IDs.

    Returns:
        Vendor pattern analysis with suspicion flags.
    """
    signals = []

    # Check for repeated vendors with high amounts
    vendor_counts = Counter(vendors)
    for vendor, count in vendor_counts.items():
        if count >= 3:
            indices = [i for i, v in enumerate(vendors) if v == vendor]
            total_amount = sum(amounts[i] for i in indices)
            signals.append({
                "signal_type": "vendor_pattern",
                "severity": "MEDIUM",
                "description": f"Vendor '{vendor}' appears {count} times with total ${round(total_amount, 2)} — possible favoritism or kickback",
                "affected_expense_ids": [expense_ids[i] for i in indices],
                "confidence": 0.72,
            })

    # Check for suspicious vendor names
    suspicious_words = ["personal", "spa", "wellness", "gift", "liquor", "casino"]
    for i, vendor in enumerate(vendors):
        if any(word in vendor.lower() for word in suspicious_words):
            signals.append({
                "signal_type": "vendor_pattern",
                "severity": "HIGH",
                "description": f"Suspicious vendor name: '{vendor}' — likely non-business expense",
                "affected_expense_ids": [expense_ids[i]],
                "confidence": 0.88,
            })

    return {
        "check": "vendor_patterns",
        "signals": signals,
        "suspicious_vendors_found": len(signals),
    }


def compute_risk_score(
    employee_id: str,
    total_amount: float,
    num_expenses: int,
    duplicate_signals: int,
    velocity_signals: int,
    vendor_signals: int,
    policy_violations: int,
    weekend_claims: int,
) -> dict:
    """
    Computes an overall fraud risk score (0-100) by aggregating all detection signals.

    Args:
        employee_id: The employee being scored.
        total_amount: Total expense amount in the report.
        num_expenses: Number of expense items.
        duplicate_signals: Number of duplicate claim signals.
        velocity_signals: Number of velocity anomaly signals.
        vendor_signals: Number of suspicious vendor signals.
        policy_violations: Number of policy violations found.
        weekend_claims: Number of weekend expense claims.

    Returns:
        Risk assessment with score, level, and recommendation.
    """
    # Weighted scoring algorithm
    score = 0

    # Duplicate claims (highest weight)
    score += min(duplicate_signals * 20, 40)

    # Policy violations
    score += min(policy_violations * 10, 25)

    # Vendor patterns
    score += min(vendor_signals * 8, 15)

    # Velocity anomalies
    score += min(velocity_signals * 5, 10)

    # Weekend claims
    score += min(weekend_claims * 5, 10)

    # High total amount bonus
    if total_amount > 5000:
        score += 5
    if total_amount > 10000:
        score += 5

    # Cap at 100
    score = min(score, 100)

    # Determine risk level
    if score >= 75:
        risk_level = "CRITICAL"
        recommendation = "ESCALATE immediately to Compliance Officer. Suspend reimbursement."
    elif score >= 50:
        risk_level = "HIGH"
        recommendation = "Flag for manual review by Finance team. Hold payment pending investigation."
    elif score >= 25:
        risk_level = "MEDIUM"
        recommendation = "Route to manager for additional approval. Request documentation."
    else:
        risk_level = "LOW"
        recommendation = "Auto-approve. No significant fraud indicators detected."

    return {
        "employee_id": employee_id,
        "risk_score": score,
        "risk_level": risk_level,
        "signals_summary": {
            "duplicates": duplicate_signals,
            "velocity": velocity_signals,
            "vendor_flags": vendor_signals,
            "policy_violations": policy_violations,
            "weekend_claims": weekend_claims,
        },
        "total_amount_reviewed": total_amount,
        "num_expenses_reviewed": num_expenses,
        "recommendation": recommendation,
    }
