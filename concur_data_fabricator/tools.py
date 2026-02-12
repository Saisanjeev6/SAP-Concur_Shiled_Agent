import uuid
import random
from datetime import datetime
import json
from typing import List, TypedDict

class ExpenseItem(TypedDict):
    expense_id: str
    employee_id: str
    category: str
    amount: float
    currency: str
    date: str
    vendor: str
    is_fraudulent: bool
# --- 1. HR & POLICY TOOLS (Used by HR_Policy_Expert) ---
def generate_persona(role: str = "Sales"):
    """Generates an employee profile for the synthetic scenario."""
    profiles = {
        "Sales": {"grade": "T3", "dept": "Global_Sales", "risk_appetite": "Medium"},
        "Executive": {"grade": "E2", "dept": "Strategy", "risk_appetite": "Low"},
        "Intern": {"grade": "I1", "dept": "Research", "risk_appetite": "High"}
    }
    profile = profiles.get(role, profiles["Sales"])
    emp_id = f"EMP-{uuid.uuid4().hex[:4].upper()}"
    return {"employee_id": emp_id, "role": role, **profile}

def get_policy_constraints(country_code: str = "US"):
    policies = {
        "US": {"meal_limit": 75.0, "hotel_limit": 350.0, "currency": "USD"},
        "DE": {"meal_limit": 60.0, "hotel_limit": 250.0, "currency": "EUR"},
        "IN": {"meal_limit": 3500.0, "hotel_limit": 12000.0, "currency": "INR"},
    }
    return policies.get(country_code, policies["US"])

# --- 2. FABRICATION TOOLS (Used by Data_Fabricator) ---
# def create_synthetic_expense(emp_id: str, policy: dict, category: str = "Meal"):
#     """Creates a realistic line item near the policy limit."""
#     limit = policy.get(f"{category.lower()}_limit", 100.0)
#     actual_amount = round(random.uniform(limit * 0.7, limit * 1.1), 2)
#     return {
#         "expense_id": f"EXP-{uuid.uuid4().hex[:6].upper()}",
#         "employee_id": emp_id,
#         "category": category,
#         "amount": actual_amount,
#         "currency": policy["currency"],
#         "vendor": f"Mock_{category}_Vendor",
#         "has_receipt": True,
#         "is_fraudulent": False
#     }
# def create_synthetic_expense(emp_id: str, policy: dict, category: str = "Meal", amount: float = None, force_over_limit: bool = False):
def create_synthetic_expense(
    emp_id: str,
    meal_limit: float,
    hotel_limit: float,
    currency: str,
    category: str = "Meal",
) -> ExpenseItem:

    limit = meal_limit if category == "Meal" else hotel_limit
    amount = round(random.uniform(limit * 0.8, limit * 0.95), 2)

    return {
        "expense_id": f"EXP-{uuid.uuid4().hex[:6].upper()}",
        "employee_id": emp_id,
        "category": category,
        "amount": amount,
        "currency": currency,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "vendor": f"Mock_{category}_Vendor_Inc",
        "is_fraudulent": False,
    }
def inject_fraud_pattern(
    expense_id: str,
    employee_id: str,
    category: str,
    amount: float,
    currency: str,
    date: str,
    vendor: str,
    pattern: str = "split_expense",
) -> List[ExpenseItem]:

    base_expense: ExpenseItem = {
        "expense_id": expense_id,
        "employee_id": employee_id,
        "category": category,
        "amount": amount,
        "currency": currency,
        "date": date,
        "vendor": vendor,
        "is_fraudulent": False,
    }

    if pattern == "split_expense":
        half = round(amount / 2, 2)

        first = base_expense.copy()
        first["amount"] = half

        second = base_expense.copy()
        second["expense_id"] = f"EXP-{uuid.uuid4().hex[:6].upper()}"
        second["amount"] = half
        second["is_fraudulent"] = True

        return [first, second]

    if pattern == "inflated_mileage":
        inflated = base_expense.copy()
        inflated["amount"] = round(amount * 1.5, 2)
        inflated["is_fraudulent"] = True
        return [inflated]

    return [base_expense]

# --- 3. VENDOR TOOLS (Used by Vendor_Verifier) ---
def verify_vendor_status(vendor_name: str, country: str):
    """Checks merchant legitimacy."""
    blacklisted = ["Shadow_Shell_Corp", "Dark_Kitchen_Ltd"]
    is_verified = vendor_name not in blacklisted
    return {
        "vendor": vendor_name, 
        "is_verified": is_verified, 
        "vendor_risk": "Low" if is_verified else "Critical"
    }

# --- 4. AUDIT TOOLS (Used by Finance_Auditor) ---
def process_approval_workflow(expense_ids: List[str], is_fraud_detected: bool = False):
    """
    Simulates the final approval gate for a batch of synthetic expenses.
    
    Args:
        expense_ids: A simple list of the ID strings (e.g., ['EXP-1', 'EXP-2']).
        is_fraud_detected: Whether any fraud was found in this batch.
    """
    if not expense_ids:
        return {"status": "error", "message": "No IDs provided."}

    status = "REJECTED" if is_fraud_detected else "APPROVED"

    return {
        "report_status": status,
        "processed_count": len(expense_ids),
        "audit_note": "Policy breach detected." if is_fraud_detected else "Clean report."
    }
# --- 5. RISK TOOLS (Used by Risk_Strategist) ---
def calculate_expense_risk(audit_results: dict, vendor_results: dict, role: str):
    """The final brain. Calculates 0-100% risk."""
    risk_score = 0
    
    # Logic Penalties
    if not audit_results.get("audit_passed"): risk_score += 0
    if vendor_results.get("vendor_risk") == "Critical": risk_score += 50
    if role == "Intern" and not audit_results.get("audit_passed"): risk_score += 10
    
    risk_score = min(risk_score, 100)
    
    # Threshold Logic
    if risk_score > 70: decision = "Manual Review"
    else: decision = "Approved"

    return {"risk_percent": risk_score, "decision": decision, "summary": f"Risk Score: {risk_score}%"}