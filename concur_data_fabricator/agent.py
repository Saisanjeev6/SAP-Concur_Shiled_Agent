from google.adk import Agent

from .tools import (
    generate_persona,
    get_policy_constraints,
    create_synthetic_expense,
    inject_fraud_pattern,
    process_approval_workflow,
)


root_agent = Agent(
    name="concur_expense_sentinel",
    model="gemini-2.5-flash",
    tools=[
        generate_persona,
        get_policy_constraints,
        create_synthetic_expense,
        inject_fraud_pattern,
        process_approval_workflow,
    ],
    instruction="""
You simulate SAP Concur expense workflows using synthetic data.

Flow:
1. Generate an employee persona
2. Fetch country-specific policy constraints
3. Create a compliant expense
4. Optionally inject fraud patterns
5. Run approval workflow
6. Return final audit decision

You must always use tools.
""",
)
