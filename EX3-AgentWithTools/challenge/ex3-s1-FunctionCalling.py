import os, time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool
import json
import datetime
import pytz
import secrets
import string 
from typing import Any, Callable, Set, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")


# Start by defining a function for your agent to call. 
# When you create a function for an agent to call, you describe its structure 
# with any required parameters in a docstring.


def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location: The location to fetch weather for.
    :return: Weather information as a JSON string.
    """
    # Mock weather data for demonstration purposes
    weather_database = {
    "New York": {"temp": "18°C", "condition": "Cloudy", "humidity": "65%"},
    "London": {"temp": "12°C", "condition": "Rainy", "humidity": "80%"},
    "Tokyo": {"temp": "22°C", "condition": "Sunny", "humidity": "55%"},
    "Sydney": {"temp": "25°C", "condition": "Partly Cloudy", "humidity": "60%"},
    "Barcelona": {"temp": "25°C", "condition": "Sunny", "humidity": "45%"}
    }       
    weather = weather_database.get(location, "Weather data not available for this location.")
    return json.dumps({"weather": weather})

def get_current_time(timezone: str = "UTC") -> str:
    """
    Gets the current time in the specified timezone.
    
    :param timezone: Timezone (UTC, EST, PST, CET, etc.)
    :return: Current time as a JSON string
    """
    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return json.dumps({"error": f"Unknown timezone: {timezone}"})
    now = datetime.datetime.now(tz)
    return json.dumps({"current_time": now.strftime("%Y-%m-%d %H:%M:%S"), "timezone": timezone})

def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """
    Generates a secure random password.
    
    :param length: Length of the password (8-50 characters)
    :param include_symbols: Whether to include special symbols (!@#$%^&*)
    :return: Generated password as a JSON string
    """
    if length < 8 or length > 50:
        return json.dumps({"error": "Password length must be between 8 and 50 characters."})
    
    alphabet = string.ascii_letters + string.digits
    symbols = "!@#$%^&*"
    password_chars = []

    if include_symbols:
        alphabet += symbols
        # Ensure at least one symbol is included
        password_chars.append(secrets.choice(symbols))
        chars_needed = length - 1
    else:
        chars_needed = length

    password_chars += [secrets.choice(alphabet) for _ in range(chars_needed)]
    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)
    return json.dumps({"password": password})

# Define user functions
user_functions = {fetch_weather, get_current_time, generate_password}

# Initialize the AIProjectClient

project_client = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=DefaultAzureCredential(),
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model=azure_foundry_deployment,
        name="Agent with Custom Function",
        instructions="You are a helpful agent",
        tools=functions.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello, send an email with the datetime and weather information in Barcelona?",
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run for the agent to handle the message
    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Created run, ID: {run.id}")

    # Poll the run status until it is completed or requires action
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                if tool_call.function.name == "fetch_weather":
                    output = fetch_weather("Barcelona")
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                elif tool_call.function.name == "get_current_time":
                    output = get_current_time("CET")
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                elif tool_call.function.name == "generate_password":
                    output = generate_password(16, True)
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                else:
                    print(f"Unknown function call: {tool_call.function.name}")  
            project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

    print(f"Run completed with status: {run.status}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message['role']}, Content: {message['content']}")

    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")