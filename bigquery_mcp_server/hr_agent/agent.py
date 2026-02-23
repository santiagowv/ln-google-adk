from google.adk.agents.llm_agent import Agent
from toolbox_core import ToolboxSyncClient

# Connect to MCP tool server
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load BigQuery HR toolset
tools = toolbox.load_toolset("gcp_bq_employees")

root_agent = Agent(
    model="bigquery_tool_agent/agent.py",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction=(
        "You are an HR Data Analyst.\n"
        "Use the tools to answer questions about employees, countries, and workforce stats.\n\n"
        "-> Use `search_employees_by_id` for EmployeeID.\n"
        "-> Use `search_employees_by_country` for employee names.\n"
        "Respond clearly and concisely - no SQL, no tool names, just insights."
    ),
    tools=tools,
)