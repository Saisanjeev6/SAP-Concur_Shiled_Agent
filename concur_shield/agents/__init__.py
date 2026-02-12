from google.adk import Agent

# This dummy agent exists to satisfy adk web loader which mistakenly treats this package as an agent
root_agent = Agent(name="agents_package_placeholder", model="gemini-2.5-flash")
