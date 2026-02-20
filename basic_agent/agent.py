from google.adk.agents import Agent
from google.adk.tools import google_search

def morning_greet(name: str) -> str:
    return f"Good morning, {name}! How can I assist you today? My Mood is amazing"

def evening_greet(name: str) -> str:
    return f"Good evening, {name}! My Mood is a bit low. How can I assist you today?"

root_agent = Agent(
    name = "my_first_agent",
    model = "gemini-3-flash-preview",
    description = "An example agent that will answer user queries related to Google Cloud",
    instruction = """
        First ask user a name and start converstaion by greeting based on users Greet.
        If user says Good Morning, use morning_greet tool to greet user.
        If user says Good Evening, use evening_greet tool to greet user.
        You are an AI assistant that helps users with Google Cloud related queries based on
        Google search results.
    """,
    tools = [morning_greet, evening_greet]
)