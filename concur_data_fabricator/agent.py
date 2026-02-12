from google.adk import Agent
from .tools import generate_persona, get_policy_constraints, create_synthetic_expense, inject_fraud_pattern, verify_vendor_status, process_approval_workflow, calculate_expense_risk    

# --- 1. HR & Policy Expert ---
hr_agent = Agent(
    name="HR_Policy_Expert",
    model="gemini-2.5-flash",
    instruction="Generates employee personas (Intern to Exec) and country-specific per-diems/limits.",
    tools=[generate_persona, get_policy_constraints]
)

# --- 2. Data Fabricator ---
fabricator_agent = Agent(
    name="Data_Fabricator",
    model="gemini-2.5-flash",
    instruction="The builder. Generates realistic line items and receipts. Can inject fraud patterns based on the inputs from the agent and also create the expenses based on the input you get like one or as many based on the input.",
    tools=[create_synthetic_expense, inject_fraud_pattern]
)

# --- 3. Vendor Verifier ---
vendor_agent = Agent(
    name="Vendor_Verifier",
    model="gemini-2.5-flash",
    instruction="Global merchant database specialist. Verifies Tax IDs and blacklisted suppliers.",
    tools=[verify_vendor_status]
)

# --- 4. Finance Auditor ---
auditor_agent = Agent(
    name="Finance_Auditor",
    model="gemini-2.5-flash",
    instruction="The rule-book keeper. Checks if the expense violates company policy or tax laws. check if the expense is for 1 day or more so based on the calculate the limit. If the same person applies more than one expense with the same by spliting sum up and cehck the limit.",
    tools=[process_approval_workflow] # Added this tool back in
)

# --- 5. Risk Strategist ---
risk_agent = Agent(
    name="Risk_Strategist",
    model="gemini-2.5-flash",
    instruction="The decision engine. Calculates final Risk % and decides: Approve (<15%), Reject (>70%), or Manual Review.",
    tools=[calculate_expense_risk]
)

# --- THE MASTER ORCHESTRATOR ---
root_agent = Agent(
    name="Concur_Mesh_Manager",
    model="gemini-2.5-flash",
    instruction="""
    You are the Lead Manager of the Synthetic Data Mesh. 
    You must orchestrate 5 specialists to build a complete Concur scenario:
    1. HR_Policy_Expert: Define WHO and the RULES.
    2. Data_Fabricator: Generate the DATA/FRAUD.
    3. Vendor_Verifier: Check the MERCHANTS.
    4. Finance_Auditor: Perform a POLICY AUDIT.
    5. Risk_Strategist: Provide the FINAL RISK SCORE & DECISION.
    Follow this SEQUENTIAL execution to prevent data loss:
    1. **Context Step 1**: Call HR_Policy_Expert. Store the persona and policy.
    2. **Context Step 2**: Call Data_Fabricator. Provide the persona and policy from Step 1 as inputs.
    3. **Context Step 3**: Call Vendor_Verifier. Provide the vendor name from the Fabricator's output.
    4. **Context Step 4**: Call Finance_Auditor. Provide BOTH the expense list (from Fabricator) and policy (from HR) as inputs.
    5. **Context Step 5**: Call Risk_Strategist. Provide the audit findings, vendor results, and role.
    If there no violations then make it as approved and if there are violations then make it as rejected/manual review based on the risk score.
    Highly important Also at the end when you have all the results, create a final summary report that includes all the details in SAP Format:
    - Employee Persona (ID, Role, Grade, Department)
    - Expense Summary (Total Amount, Categories)
    - Vendor Legitimacy (Verified/Unverified)
    - Audit Findings (Passed/Failed, Violations)
    - Final Risk Score and Decision (Approve/Reject/Manual Review)
    """,
    sub_agents=[hr_agent, fabricator_agent, vendor_agent, auditor_agent, risk_agent]
)