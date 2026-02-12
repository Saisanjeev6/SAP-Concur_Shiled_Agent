import uuid
import random
from datetime import datetime
from typing import TypedDict, List


# =========================
# DATA MODELS (STRICT)
# =========================

class Persona(TypedDict):
    employee_id: str
    name: str
    role: str
    grade: str
    dept: str
    risk_appetite: str


class Policy(TypedDict):
    meal_limit: float
    hotel_limit: float
    currency: str


class ExpenseItem(TypedDict):
    expense_id: str
    employee_id: str
    category: str
    amount: float
    currency: str
    date: str
    vendor: str
    is_fraudulent: bool


class ApprovalResult(TypedDict):
    report_status: str
    total_items: int
    audit_flags: int
    comments: str


# =========================
# 1. PERSONA TOOL
# =========================

def generate_persona(role: str = "Sales") -> Persona:
    profiles = {
        "Sales": {"grade": "T3", "dept": "Global_Sales", "risk_appetite": "Medium"},
        "Executive": {"grade": "E2", "dept": "Strategy", "risk_appetite": "Low"},
        "Consultant": {"grade": "C4", "dept": "Delivery", "risk_appetite": "High"},
    }

    profile = profiles.get(role, profiles["Sales"])
    emp_id = f"EMP-{uuid.uuid4().hex[:4].upper()}"

    return {
        "employee_id": emp_id,
        "name": f"Synthetic_User_{emp_id}",
        "role": role,
        "grade": profile["grade"],
        "dept": profile["dept"],
        "risk_appetite": profile["risk_appetite"],
    }


# =========================
# 2. POLICY TOOL
# =========================

def get_policy_constraints(country_code: str = "US") -> Policy:
    policies = {
        "US": {"meal_limit": 75.0, "hotel_limit": 350.0, "currency": "USD"},
        "DE": {"meal_limit": 60.0, "hotel_limit": 250.0, "currency": "EUR"},
        "IN": {"meal_limit": 3500.0, "hotel_limit": 12000.0, "currency": "INR"},
    }
    return policies.get(country_code, policies["US"])


# =========================
# 3. EXPENSE GENERATOR TOOL
# =========================

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

# =========================
# 4. FRAUD SIMULATION TOOL
# =========================

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


# =========================
# 5. APPROVAL WORKFLOW TOOL
# =========================

from typing import List

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