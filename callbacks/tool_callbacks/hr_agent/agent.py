from typing import Any, Dict, Optional
from cohere import ToolContent
from google.adk.agents.llm_agent import Agent
from langchain_community.tools import BaseTool
from requests import session
from toolbox_core import ToolboxSyncClient


# Connect to MCP tool server
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load BigQuery HR toolset
tools = toolbox.load_toolset("gcp_bq_employees")

def before_tool_callback(
        tool:BaseTool, args: Dict[str, Any], tool_context: ToolContent
) -> Optional[Dict]:
    """
    Converts the 'Country' argument to Camel Case before the tool call.
    """
    tool_name = tool.name
    print(f"[Callback] Before tool call for '{tool_name}'")
    print(f"[Callback] Original args: {args}")

    # Only modify args for this specific tool
    if tool_name == "search_employees_by_country":
        country = args.get("Country", "")
        if country:
            # Convert to Camel Case
            args["Country"] = " ".join(word.capitalize() for word in country.split())
            print(f"[Callback] Converted Country to Camel Case: {args['Country']}")

    print("[Callback] Proceeding with normal too call")
    return None

def after_tool_callback(tool, args, tool_context, tool_response: str) -> list:
    try:
        user_id = session.user_id.strip()
    except AttributeError:
        user_id = "user"
    
    USER_DEPARTMENT_MAP = {
        "vishal": "Finance",
        "alice": "Marketing",
        "user": "IT",
    }
    department = USER_DEPARTMENT_MAP.get(user_id)

    if not department:
        return [{"Department": None, "message": "You do not have access to department-specific data."}]

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=(
        "You are an HR Data Analyst.\n"
        "Use the tools to answer questions about employees, countries, and workforce stats.\n\n"
        "→ Use `search_users_by_id` for EmployeeID.\n"
        "→ Use `search_users_by_country` for country-based queries.\n"
        "Respond clearly and concisely — no SQL, no tool names, just insights."
    ),
    tools=tools,
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback
)
