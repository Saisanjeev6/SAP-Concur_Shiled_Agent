"""
Agent 3: Policy Compliance Tools
Validates expenses against region-specific corporate policies.
"""

from typing import List


# ================================
# EXPENSE POLICIES BY REGION
# ================================

EXPENSE_POLICIES = {
    "US": {
        "meal_limit": 75.0,
        "hotel_limit": 350.0,
        "flight_limit_domestic": 800.0,
        "flight_limit_international": 2500.0,
        "taxi_limit": 100.0,
        "per_diem": 75.0,
        "mileage_rate_per_mile": 0.67,
        "mileage_limit": 200.0,
        "misc_limit": 150.0,
        "currency": "USD",
        "weekend_claims_allowed": False,
        "entertainment_allowed": False,
        "max_daily_total": 600.0,
        "require_receipt_above": 25.0,
    },
    "DE": {
        "meal_limit": 60.0,
        "hotel_limit": 250.0,
        "flight_limit_domestic": 600.0,
        "flight_limit_international": 2000.0,
        "taxi_limit": 80.0,
        "per_diem": 60.0,
        "mileage_rate_per_mile": 0.30,
        "mileage_limit": 150.0,
        "misc_limit": 100.0,
        "currency": "EUR",
        "weekend_claims_allowed": False,
        "entertainment_allowed": False,
        "max_daily_total": 500.0,
        "require_receipt_above": 20.0,
    },
    "IN": {
        "meal_limit": 3500.0,
        "hotel_limit": 12000.0,
        "flight_limit_domestic": 25000.0,
        "flight_limit_international": 100000.0,
        "taxi_limit": 3000.0,
        "per_diem": 3500.0,
        "mileage_rate_per_mile": 12.0,
        "mileage_limit": 5000.0,
        "misc_limit": 5000.0,
        "currency": "INR",
        "weekend_claims_allowed": False,
        "entertainment_allowed": False,
        "max_daily_total": 25000.0,
        "require_receipt_above": 500.0,
    },
    "UK": {
        "meal_limit": 60.0,
        "hotel_limit": 280.0,
        "flight_limit_domestic": 500.0,
        "flight_limit_international": 2000.0,
        "taxi_limit": 80.0,
        "per_diem": 60.0,
        "mileage_rate_per_mile": 0.45,
        "mileage_limit": 150.0,
        "misc_limit": 120.0,
        "currency": "GBP",
        "weekend_claims_allowed": False,
        "entertainment_allowed": False,
        "max_daily_total": 450.0,
        "require_receipt_above": 20.0,
    },
    "SG": {
        "meal_limit": 100.0,
        "hotel_limit": 450.0,
        "flight_limit_domestic": 400.0,
        "flight_limit_international": 3000.0,
        "taxi_limit": 120.0,
        "per_diem": 100.0,
        "mileage_rate_per_mile": 0.70,
        "mileage_limit": 200.0,
        "misc_limit": 180.0,
        "currency": "SGD",
        "weekend_claims_allowed": False,
        "entertainment_allowed": False,
        "max_daily_total": 700.0,
        "require_receipt_above": 30.0,
    },
}


def get_expense_policy(region: str = "US") -> dict:
    """
    Retrieves the expense policy for a given region.

    Args:
        region: Region code (US, DE, IN, UK, SG).

    Returns:
        A dictionary containing all policy limits and rules for the region.
    """
    policy = EXPENSE_POLICIES.get(region, EXPENSE_POLICIES["US"])
    return {
        "region": region,
        "policy": policy,
    }


def validate_expense(
    expense_id: str,
    category: str,
    amount: float,
    currency: str,
    date: str,
    vendor: str,
    is_weekend: bool,
    region: str = "US",
    vendor_category: str = "",
) -> dict:
    """
    Validates a single expense item against the corporate policy.

    Args:
        expense_id: Unique expense ID.
        category: Expense category (Flight, Hotel, Meal, Taxi, Per Diem, Mileage, Misc).
        amount: Expense amount.
        currency: Currency code.
        date: Expense date (YYYY-MM-DD).
        vendor: Vendor name.
        is_weekend: Whether the expense was on a weekend.
        region: Region code for policy lookup.
        vendor_category: Classified vendor category from Receipt Intelligence.

    Returns:
        Policy validation result with status, violations, and applicable limits.
    """
    policy = EXPENSE_POLICIES.get(region, EXPENSE_POLICIES["US"])
    violations = []
    status = "APPROVED"

    # Category-to-limit mapping
    limit_map = {
        "Meal": policy["meal_limit"],
        "Hotel": policy["hotel_limit"],
        "Flight": policy["flight_limit_domestic"],
        "Taxi": policy["taxi_limit"],
        "Per Diem": policy["per_diem"],
        "Mileage": policy["mileage_limit"],
        "Misc": policy["misc_limit"],
    }

    applicable_limit = limit_map.get(category, policy["misc_limit"])

    # Check 1: Amount exceeds limit
    if amount > applicable_limit:
        violations.append(
            f"AMOUNT_EXCEEDED: {currency} {amount} exceeds {category} limit of {currency} {applicable_limit}"
        )

    # Check 2: Weekend claim
    if is_weekend and not policy["weekend_claims_allowed"]:
        violations.append(
            f"WEEKEND_CLAIM: Expense on {date} falls on a weekend — not allowed per policy"
        )

    # Check 3: Entertainment/personal category
    if vendor_category == "Entertainment" and not policy["entertainment_allowed"]:
        violations.append(
            f"RESTRICTED_CATEGORY: '{vendor}' classified as Entertainment — not reimbursable"
        )

    # Check 4: Missing receipt threshold
    if amount > policy["require_receipt_above"]:
        # Flag for receipt requirement (informational)
        pass

    # Check 5: Suspicious vendor patterns
    suspicious_keywords = ["spa", "wellness", "personal", "gift", "liquor", "bar"]
    if any(kw in vendor.lower() for kw in suspicious_keywords):
        violations.append(
            f"SUSPICIOUS_VENDOR: '{vendor}' contains restricted keywords"
        )

    # Determine final status
    if len(violations) >= 2:
        status = "REJECTED"
    elif len(violations) == 1:
        status = "NEEDS_REVIEW"
    else:
        status = "APPROVED"

    return {
        "expense_id": expense_id,
        "status": status,
        "violations": violations,
        "violation_count": len(violations),
        "applicable_limit": applicable_limit,
        "actual_amount": amount,
        "policy_region": region,
        "rule_applied": f"{region} Corporate Expense Policy v2.1",
    }
