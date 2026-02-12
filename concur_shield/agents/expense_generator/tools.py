"""
Agent 1: Synthetic Expense Generator
Generates realistic employee profiles and diverse expense reports.
Can optionally inject anomalies for fraud testing.
"""

import random
import json
from concur_shield.shared.utils import (
    generate_employee_id, generate_expense_id, generate_receipt_number,
    random_date, is_weekend, random_vendor, random_city,
    random_employee_name, random_department, random_grade, random_manager,
)


def generate_employee_profile(
    region: str = "US",
    department: str = "",
    risk_tier: str = "Medium",
) -> dict:
    """
    Generates a realistic synthetic employee profile.

    Args:
        region: Employee region code (US, DE, IN, UK, SG).
        department: Department name. Leave empty for random assignment.
        risk_tier: Risk tier for the employee (Low, Medium, High).

    Returns:
        A dictionary with the full employee profile.
    """
    emp_id = generate_employee_id()
    name = random_employee_name()
    dept = department if department else random_department()

    return {
        "employee_id": emp_id,
        "name": name,
        "email": f"{name.lower().replace(' ', '.')}@acme-corp.com",
        "department": dept,
        "grade": random_grade(),
        "region": region,
        "cost_center": f"CC-{random.randint(1000, 9999)}",
        "manager": random_manager(),
        "risk_tier": risk_tier,
    }


def generate_expense_report(
    employee_id: str,
    employee_name: str,
    region: str = "US",
    num_items: int = 1,
    include_anomalies: bool = False,
    trip_purpose: str = "Client Meeting",
) -> dict:
    """
    Generates a synthetic expense report with multiple line items.

    Args:
        employee_id: The employee ID to attach expenses to.
        employee_name: Name of the employee.
        region: Region for currency and policy context (US, DE, IN).
        num_items: Number of expense items to generate (1-10).
        include_anomalies: If True, inject 1-2 suspicious expense items.
        trip_purpose: Business purpose for the trip.

    Returns:
        A dictionary with the expense report containing all line items.
    """
    num_items = max(1, min(num_items, 10))

    currency_map = {"US": "USD", "DE": "EUR", "IN": "INR", "UK": "GBP", "SG": "SGD"}
    currency = currency_map.get(region, "USD")

    # Amount ranges per category (in USD equivalent)
    amount_ranges = {
        "Flight": (200, 1500),
        "Hotel": (120, 450),
        "Meal": (15, 95),
        "Taxi": (10, 75),
        "Per Diem": (50, 100),
        "Mileage": (20, 150),
        "Misc": (5, 200),
    }

    # Currency multipliers
    multipliers = {"USD": 1.0, "EUR": 0.92, "INR": 83.0, "GBP": 0.79, "SGD": 1.34}
    mult = multipliers.get(currency, 1.0)

    categories = ["Flight", "Hotel", "Meal", "Meal", "Taxi", "Per Diem", "Mileage", "Misc"]
    expense_items = []

    for i in range(num_items):
        category = random.choice(categories)
        low, high = amount_ranges[category]
        amount = round(random.uniform(low, high) * mult, 2)
        date = random_date(days_back=21)
        city = random_city()
        vendor = random_vendor(category)

        item = {
            "expense_id": generate_expense_id(),
            "employee_id": employee_id,
            "category": category,
            "subcategory": f"{category} - Business",
            "amount": amount,
            "currency": currency,
            "date": date,
            "vendor": vendor,
            "city": city,
            "description": f"{category} expense for {trip_purpose} in {city}",
            "receipt_number": generate_receipt_number(),
            "is_weekend": is_weekend(date),
            "is_anomaly": False,
            "anomaly_type": None,
        }
        expense_items.append(item)

    # Inject anomalies if requested
    if include_anomalies and len(expense_items) >= 2:
        anomaly_count = random.randint(1, min(2, len(expense_items)))
        anomaly_types = ["duplicate", "inflated", "out_of_policy", "weekend_claim"]

        for idx in random.sample(range(len(expense_items)), anomaly_count):
            anomaly = random.choice(anomaly_types)
            expense_items[idx]["is_anomaly"] = True
            expense_items[idx]["anomaly_type"] = anomaly

            if anomaly == "inflated":
                expense_items[idx]["amount"] = round(expense_items[idx]["amount"] * 2.5, 2)
                expense_items[idx]["description"] = f"[INFLATED] {expense_items[idx]['description']}"

            elif anomaly == "duplicate":
                # Keep report size stable: reuse an existing second item and copy receipt number.
                target_indices = [i for i in range(len(expense_items)) if i != idx]
                if target_indices:
                    target_idx = random.choice(target_indices)
                    expense_items[target_idx]["receipt_number"] = expense_items[idx]["receipt_number"]
                    expense_items[target_idx]["is_anomaly"] = True
                    expense_items[target_idx]["anomaly_type"] = "duplicate"

            elif anomaly == "out_of_policy":
                expense_items[idx]["category"] = "Misc"
                expense_items[idx]["vendor"] = "Personal Spa & Wellness"
                expense_items[idx]["subcategory"] = "Personal Entertainment"
                expense_items[idx]["amount"] = round(random.uniform(300, 800) * mult, 2)

            elif anomaly == "weekend_claim":
                # Force a weekend date
                import datetime as dt
                today = dt.datetime.now()
                # Find next Saturday
                days_until_sat = (5 - today.weekday()) % 7
                if days_until_sat == 0:
                    days_until_sat = 7
                weekend_date = today - dt.timedelta(days=random.randint(1, 3) * 7 - days_until_sat)
                expense_items[idx]["date"] = weekend_date.strftime("%Y-%m-%d")
                expense_items[idx]["is_weekend"] = True

    total_amount = round(sum(item["amount"] for item in expense_items), 2)

    return {
        "report_id": f"RPT-{employee_id.split('-')[1]}-{random.randint(100, 999)}",
        "employee_id": employee_id,
        "employee_name": employee_name,
        "region": region,
        "currency": currency,
        "trip_purpose": trip_purpose,
        "total_amount": total_amount,
        "total_items": len(expense_items),
        "submission_date": random_date(days_back=3),
        "expense_items": expense_items,
    }


def inject_anomaly(
    expense_id: str,
    employee_id: str,
    category: str,
    amount: float,
    currency: str,
    date: str,
    vendor: str,
    anomaly_type: str = "duplicate",
) -> list:
    """
    Injects a specific fraud anomaly into an expense item.

    Args:
        expense_id: The expense ID to modify.
        employee_id: The employee ID.
        category: Expense category.
        amount: Original expense amount.
        currency: Currency code.
        date: Expense date (YYYY-MM-DD).
        vendor: Vendor name.
        anomaly_type: Type of anomaly: 'duplicate', 'inflated', 'split_expense', 'weekend_claim'.

    Returns:
        A list of modified expense items with the anomaly injected.
    """
    base = {
        "expense_id": expense_id,
        "employee_id": employee_id,
        "category": category,
        "subcategory": f"{category} - Business",
        "amount": amount,
        "currency": currency,
        "date": date,
        "vendor": vendor,
        "city": random_city(),
        "description": f"Anomaly-injected {category} expense",
        "receipt_number": generate_receipt_number(),
        "is_weekend": is_weekend(date),
        "is_anomaly": True,
        "anomaly_type": anomaly_type,
    }

    if anomaly_type == "duplicate":
        dup = base.copy()
        dup["expense_id"] = generate_expense_id()
        return [base, dup]

    elif anomaly_type == "inflated":
        base["amount"] = round(amount * 2.5, 2)
        return [base]

    elif anomaly_type == "split_expense":
        half = round(amount / 2, 2)
        first = base.copy()
        first["amount"] = half
        second = base.copy()
        second["expense_id"] = generate_expense_id()
        second["amount"] = half
        return [first, second]

    elif anomaly_type == "weekend_claim":
        base["is_weekend"] = True
        return [base]

    return [base]
