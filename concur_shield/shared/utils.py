"""
ConcurShield AI — Shared Utilities
Helper functions and data pools used across agents.
"""

import uuid
import random
from datetime import datetime, timedelta


# ================================
# ID GENERATORS
# ================================

def generate_id(prefix: str = "CS") -> str:
    """Generate a unique ID with a given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


def generate_employee_id() -> str:
    return generate_id("EMP")


def generate_expense_id() -> str:
    return generate_id("EXP")


def generate_report_id() -> str:
    return generate_id("RPT")


def generate_receipt_number() -> str:
    return generate_id("RCT")


# ================================
# DATE UTILITIES
# ================================

def random_date(days_back: int = 30) -> str:
    """Generate a random date within the last N days."""
    offset = random.randint(0, days_back)
    dt = datetime.now() - timedelta(days=offset)
    return dt.strftime("%Y-%m-%d")


def is_weekend(date_str: str) -> bool:
    """Check if a date string (YYYY-MM-DD) falls on a weekend."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.weekday() >= 5  # Saturday=5, Sunday=6


def current_timestamp() -> str:
    """Return current UTC timestamp as ISO string."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


# ================================
# DATA POOLS
# ================================

VENDORS = {
    "Meal": [
        "The Capital Grille", "Olive Garden", "Chipotle Mexican Grill",
        "PF Chang's", "Starbucks", "Panera Bread", "Shake Shack",
        "Nobu Restaurant", "Ruth's Chris Steakhouse", "Subway",
    ],
    "Hotel": [
        "Marriott International", "Hilton Hotels", "Hyatt Regency",
        "Four Seasons", "InterContinental", "Holiday Inn Express",
        "Westin Hotels", "Sheraton Hotels", "Courtyard by Marriott",
        "Ritz-Carlton",
    ],
    "Flight": [
        "United Airlines", "Delta Air Lines", "American Airlines",
        "Southwest Airlines", "JetBlue Airways", "Lufthansa",
        "British Airways", "Emirates", "Singapore Airlines", "Air India",
    ],
    "Taxi": [
        "Uber Business", "Lyft Corporate", "Yellow Cab Co.",
        "City Taxi Services", "Executive Car Service",
    ],
    "Mileage": [
        "Personal Vehicle Reimbursement",
    ],
    "Per Diem": [
        "Daily Allowance",
    ],
    "Misc": [
        "FedEx Office", "Staples", "Office Depot", "Amazon Business",
        "Best Buy Business", "Conference Registration",
    ],
}

CITIES = [
    "New York", "San Francisco", "Chicago", "Los Angeles", "Boston",
    "Seattle", "Austin", "Denver", "Miami", "Atlanta",
    "Dallas", "Washington DC", "Philadelphia", "Phoenix", "Houston",
    "Munich", "London", "Bangalore", "Singapore", "Tokyo",
]

DEPARTMENTS = [
    "Global Sales", "Engineering", "Marketing", "Finance",
    "Human Resources", "Strategy", "Consulting", "Operations",
    "Product Management", "Customer Success",
]

EMPLOYEE_NAMES = [
    "Aisha Patel", "Marco Rossi", "Sarah Chen", "James O'Brien",
    "Maria Garcia", "Kenji Tanaka", "Elena Volkov", "David Kim",
    "Priya Sharma", "Thomas Mueller", "Olivia Johnson", "Raj Krishnan",
    "Sophie Martin", "Ahmed Hassan", "Lisa Wong", "Carlos Rivera",
]

GRADES = ["E1", "E2", "E3", "T1", "T2", "T3", "C1", "C2", "C3", "C4"]

MANAGER_NAMES = [
    "VP Sarah Mitchell", "Dir. Robert Chang", "SVP Amanda Foster",
    "Dir. Michael Torres", "VP Jennifer Adams",
]


def random_vendor(category: str) -> str:
    """Return a random vendor for a given expense category."""
    vendors = VENDORS.get(category, VENDORS["Misc"])
    return random.choice(vendors)


def random_city() -> str:
    return random.choice(CITIES)


def random_department() -> str:
    return random.choice(DEPARTMENTS)


def random_employee_name() -> str:
    return random.choice(EMPLOYEE_NAMES)


def random_grade() -> str:
    return random.choice(GRADES)


def random_manager() -> str:
    return random.choice(MANAGER_NAMES)
