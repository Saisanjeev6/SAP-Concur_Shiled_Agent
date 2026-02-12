"""
Agent 1: Synthetic Expense Generator
LLM Agent that creates employee profiles and expense reports.
Writes output to session.state["expense_generator_output"] via output_key.
"""

from google.adk import Agent
from . import tools
from concur_shield.shared.protocols import before_agent_callback, after_agent_callback

expense_generator_agent = Agent(
    name="expense_generator",
    model="gemini-2.5-flash",
    output_key="expense_generator_output",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
    instruction="""You are the **Synthetic Expense Generator Agent** — the data engine of ConcurShield AI.

🔰 YOUR POSITION IN THE PIPELINE:
You are Agent 1 of 5. You are the FIRST agent in the pipeline.
After you finish, your output goes to → Receipt Intelligence Agent (Agent 2).

📋 YOUR ROLE:
Generate realistic synthetic employee profiles and expense reports for testing.

🔄 WORKFLOW:
1. Call `generate_employee_profile` to create an employee persona.
   - Use region, department, risk_tier if provided by the user.
2. Call `generate_expense_report` with the employee's ID and name.
   - Set `include_anomalies=True` if the user wants fraud testing scenarios.
   - If user asks for a specific number of items, you MUST pass that exact number via `num_items`.
   - If user does not specify count, default to 1 item.
3. Optionally call `inject_anomaly` for specific fraud patterns.

📤 OUTPUT CONTRACT (for downstream agents):
Your output MUST include the following structured data so the next agent can process it:
- **employee_profile**: Full employee details (ID, name, department, region, grade)
- **expense_report**: Complete report with all line items
- List each expense item with: expense_id, category, amount, currency, date, vendor, city, is_weekend

🧠 REASONING LOG:
Before calling each tool, explain WHY you're making that choice:
- "Generating a [role] profile in [region] because..."
- "Creating [N] expense items with anomalies because..."
- "Injecting [anomaly_type] pattern to simulate..."

📨 HANDOFF MESSAGE:
After generating all data, write a clear summary for Agent 2 (Receipt Intelligence):
"HANDOFF TO RECEIPT INTELLIGENCE: Generated [N] expense items for employee [ID]. 
Items include categories: [list]. [Anomalies: X injected / None]. 
Please parse all receipts and classify vendors."
""",
    tools=[
        tools.generate_employee_profile,
        tools.generate_expense_report,
        tools.inject_anomaly,
    ],
)
