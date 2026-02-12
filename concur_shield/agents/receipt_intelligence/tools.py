"""
Agent 2: Receipt Intelligence Tools
NLP-powered receipt parsing and enrichment.
"""

import random
from concur_shield.shared.utils import generate_id


# Merchant Category Code mapping
MERCHANT_CODES = {
    "Restaurant": "MCC-5812",
    "Hotel": "MCC-7011",
    "Airline": "MCC-4511",
    "Transport": "MCC-4121",
    "Retail": "MCC-5999",
    "Entertainment": "MCC-7941",
    "Fuel": "MCC-5541",
    "Office": "MCC-5943",
    "Other": "MCC-0000",
}

VENDOR_CATEGORY_MAP = {
    "Capital Grille": "Restaurant",
    "Olive Garden": "Restaurant",
    "Chipotle": "Restaurant",
    "Chang": "Restaurant",
    "Starbucks": "Restaurant",
    "Panera": "Restaurant",
    "Shake Shack": "Restaurant",
    "Nobu": "Restaurant",
    "Ruth's Chris": "Restaurant",
    "Subway": "Restaurant",
    "Marriott": "Hotel",
    "Hilton": "Hotel",
    "Hyatt": "Hotel",
    "Four Seasons": "Hotel",
    "InterContinental": "Hotel",
    "Holiday Inn": "Hotel",
    "Westin": "Hotel",
    "Sheraton": "Hotel",
    "Courtyard": "Hotel",
    "Ritz-Carlton": "Hotel",
    "United Airlines": "Airline",
    "Delta": "Airline",
    "American Airlines": "Airline",
    "Southwest": "Airline",
    "JetBlue": "Airline",
    "Lufthansa": "Airline",
    "British Airways": "Airline",
    "Emirates": "Airline",
    "Singapore Airlines": "Airline",
    "Air India": "Airline",
    "Uber": "Transport",
    "Lyft": "Transport",
    "Yellow Cab": "Transport",
    "Taxi": "Transport",
    "Car Service": "Transport",
    "Spa": "Entertainment",
    "Wellness": "Entertainment",
    "FedEx": "Office",
    "Staples": "Office",
    "Office Depot": "Office",
    "Amazon": "Retail",
    "Best Buy": "Retail",
}

PAYMENT_METHODS = [
    "Corporate Card (Visa)",
    "Corporate Card (Amex)",
    "Personal Card (Reimbursement)",
    "Cash",
    "Wire Transfer",
]


def _classify_vendor(vendor_name: str) -> str:
    """Classify a vendor into a category using keyword matching."""
    for keyword, category in VENDOR_CATEGORY_MAP.items():
        if keyword.lower() in vendor_name.lower():
            return category
    return "Other"


def parse_receipt(
    expense_id: str,
    vendor: str,
    amount: float,
    currency: str,
    date: str,
    category: str,
    city: str = "",
) -> dict:
    """
    Parses a synthetic receipt and extracts structured data using NLP logic.

    Args:
        expense_id: The expense ID this receipt belongs to.
        vendor: Vendor or merchant name.
        amount: Transaction amount.
        currency: Currency code.
        date: Transaction date (YYYY-MM-DD).
        category: Original expense category.
        city: City where the transaction occurred.

    Returns:
        Structured receipt data with vendor classification, merchant code, and confidence score.
    """
    vendor_category = _classify_vendor(vendor)
    merchant_code = MERCHANT_CODES.get(vendor_category, "MCC-0000")

    # Determine if it's a weekend
    from concur_shield.shared.utils import is_weekend
    weekend = is_weekend(date)

    # Simulate confidence based on data quality
    confidence = round(random.uniform(0.85, 0.99), 2)
    if vendor_category == "Other":
        confidence = round(random.uniform(0.60, 0.82), 2)

    return {
        "expense_id": expense_id,
        "vendor_name": vendor,
        "vendor_category": vendor_category,
        "merchant_code": merchant_code,
        "transaction_date": date,
        "amount": amount,
        "currency": currency,
        "payment_method": random.choice(PAYMENT_METHODS),
        "city": city,
        "is_weekend": weekend,
        "confidence_score": confidence,
    }


def enrich_receipt_metadata(
    expense_id: str,
    vendor_name: str,
    vendor_category: str,
    amount: float,
    city: str,
    is_weekend: bool,
) -> dict:
    """
    Enriches receipt data with additional metadata flags for downstream analysis.

    Args:
        expense_id: The expense ID.
        vendor_name: Name of the vendor.
        vendor_category: Classified vendor category.
        amount: Transaction amount.
        city: Transaction city.
        is_weekend: Whether the transaction occurred on a weekend.

    Returns:
        Enriched metadata with risk flags and additional context.
    """
    flags = []

    if is_weekend:
        flags.append("WEEKEND_TRANSACTION")

    if vendor_category == "Entertainment":
        flags.append("NON_BUSINESS_CATEGORY")

    if amount > 500:
        flags.append("HIGH_VALUE_TRANSACTION")

    if amount > 1000:
        flags.append("VERY_HIGH_VALUE")

    if vendor_category == "Other":
        flags.append("UNCLASSIFIED_VENDOR")

    # International transaction check
    international_cities = ["Munich", "London", "Bangalore", "Singapore", "Tokyo"]
    if city in international_cities:
        flags.append("INTERNATIONAL_TRANSACTION")

    return {
        "expense_id": expense_id,
        "vendor_name": vendor_name,
        "vendor_category": vendor_category,
        "enrichment_flags": flags,
        "flag_count": len(flags),
        "requires_additional_review": len(flags) >= 2,
        "city_type": "International" if city in international_cities else "Domestic",
    }
