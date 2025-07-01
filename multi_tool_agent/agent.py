import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types  # For creating message Content/Parts
import os
import warnings
import asyncio
from typing import Optional  # Make sure to import Optional

# Ignore all warnings
warnings.filterwarnings("ignore")

# @title Configure API Keys (Replace with your actual keys!)

# --- IMPORTANT: Using Vertex AI for all models ---

# Configure for Vertex AI authentication (recommended for production)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Set your Google Cloud project ID
os.environ["GOOGLE_CLOUD_PROJECT"] = "adk-tutorial-464514"  # <--- REPLACE with your GCP project ID

# Set the region for Vertex AI
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"  # <--- REPLACE with your preferred region

# --- Verify Configuration ---
print("Configuration:")
print(f"Using Vertex AI: {'Yes' if os.environ.get('GOOGLE_GENAI_USE_VERTEXAI') == 'True' else 'No'}")
print(f"Project ID: {os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not set')}")
print(f"Location: {os.environ.get('GOOGLE_CLOUD_LOCATION', 'Not set')}")

# For Vertex AI, you'll need to authenticate using one of these methods:
# 1. Application Default Credentials (ADC) - recommended
#    - Run: gcloud auth application-default login
#    - Or set GOOGLE_APPLICATION_CREDENTIALS to your service account key file
# 2. Service Account Key
#    - Set: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-key.json"

# Check if we have authentication set up
try:
    import google.auth
    credentials, project = google.auth.default()
    print(f"✓ Authentication available for project: {project}")
except Exception as e:
    print(f"⚠ Authentication issue: {e}")
    print("Please run: gcloud auth application-default login")
    print("Or set GOOGLE_APPLICATION_CREDENTIALS to your service account key file")

# --- Define Model Constants for easier use ---

# Google models available through Vertex AI
# More supported models can be referenced here: https://ai.google.dev/gemini-api/docs/models#model-variations
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_0_FLASH_001 = "gemini-2.0-flash-001"
MODEL_GEMINI_1_5_PRO = "gemini-1.5-pro"
MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Set default model for agents
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH  # Using Gemini 2.0 Flash as default

print("\nEnvironment configured.")


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        greeting = "Hello there!"  # Default greeting if name is None or not explicitly passed
        print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
    return greeting


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."


print("Greeting and Farewell tools defined.")

# Optional self-test
print(say_hello("Alice"))
print(say_hello())  # Test with no argument (should use default "Hello there!")
print(say_hello(name=None))  # Test with name explicitly as None (should use default "Hello there!")

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)

# Weather-only agent for more focused weather queries
weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL,  # Using the default Google model
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather],
)

print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"  # Using a fixed ID for simplicity

# Create the specific session where the conversation will happen
async def setup_session():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    return session

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=weather_agent,  # The agent we want to run
    app_name=APP_NAME,    # Associates runs with our app
    session_service=session_service  # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")

# We need an async function to await our interaction helper
async def run_conversation():
    # Create the session first
    await setup_session()
    
    await call_agent_async("What is the weather like in London?",
                          runner=runner,
                          user_id=USER_ID,
                          session_id=SESSION_ID)

    await call_agent_async("How about Paris?",
                          runner=runner,
                          user_id=USER_ID,
                          session_id=SESSION_ID)  # Expecting the tool's error message

    await call_agent_async("Tell me the weather in New York",
                          runner=runner,
                          user_id=USER_ID,
                          session_id=SESSION_ID)

# Execute the conversation using await in an async context (like Colab/Jupyter)
# await run_conversation()

# --- OR ---

# Uncomment the following lines if running as a standard Python script (.py file):
# if __name__ == "__main__":
#     try:
#         asyncio.run(run_conversation())
#     except Exception as e:
#         print(f"An error occurred: {e}")

# @title Define and Test Multiple Google Models

# Make sure 'get_weather' function from Step 1 is defined in your environment.
# Make sure 'call_agent_async' is defined from earlier.

# --- Agent using Gemini 1.5 Pro ---
weather_agent_gemini_pro = None  # Initialize to None
runner_gemini_pro = None      # Initialize runner to None

async def test_gemini_pro_agent():
    try:
        weather_agent_gemini_pro = Agent(
            name="weather_agent_gemini_pro",
            model=MODEL_GEMINI_1_5_PRO,  # Using Gemini 1.5 Pro
            description="Provides weather information (using Gemini 1.5 Pro).",
            instruction="You are a helpful weather assistant powered by Gemini 1.5 Pro. "
                        "Use the 'get_weather' tool for city weather requests. "
                        "Clearly present successful reports or polite error messages based on the tool's output status.",
            tools=[get_weather],  # Re-use the same tool
        )
        print(f"Agent '{weather_agent_gemini_pro.name}' created using model '{MODEL_GEMINI_1_5_PRO}'.")

        # InMemorySessionService is simple, non-persistent storage for this tutorial.
        session_service_gemini_pro = InMemorySessionService()  # Create a dedicated service

        # Define constants for identifying the interaction context
        APP_NAME_GEMINI_PRO = "weather_tutorial_app_gemini_pro"  # Unique app name for this test
        USER_ID_GEMINI_PRO = "user_1_gemini_pro"
        SESSION_ID_GEMINI_PRO = "session_001_gemini_pro"  # Using a fixed ID for simplicity

        # Create the specific session where the conversation will happen
        session_gemini_pro = await session_service_gemini_pro.create_session(
            app_name=APP_NAME_GEMINI_PRO,
            user_id=USER_ID_GEMINI_PRO,
            session_id=SESSION_ID_GEMINI_PRO
        )
        print(f"Session created: App='{APP_NAME_GEMINI_PRO}', User='{USER_ID_GEMINI_PRO}', Session='{SESSION_ID_GEMINI_PRO}'")

        # Create a runner specific to this agent and its session service
        runner_gemini_pro = Runner(
            agent=weather_agent_gemini_pro,
            app_name=APP_NAME_GEMINI_PRO,       # Use the specific app name
            session_service=session_service_gemini_pro  # Use the specific session service
        )
        print(f"Runner created for agent '{runner_gemini_pro.agent.name}'.")

        # --- Test the Gemini Pro Agent ---
        print("\n--- Testing Gemini 1.5 Pro Agent ---")
        # Ensure call_agent_async uses the correct runner, user_id, session_id
        await call_agent_async(query="What's the weather in Tokyo?",
                               runner=runner_gemini_pro,
                               user_id=USER_ID_GEMINI_PRO,
                               session_id=SESSION_ID_GEMINI_PRO)

    except Exception as e:
        print(f"❌ Could not create or run Gemini Pro agent '{MODEL_GEMINI_1_5_PRO}'. Error: {e}")

# --- Agent using Gemini 1.5 Flash ---
weather_agent_gemini_flash = None  # Initialize to None
runner_gemini_flash = None      # Initialize runner to None

async def test_gemini_flash_agent():
    try:
        weather_agent_gemini_flash = Agent(
            name="weather_agent_gemini_flash",
            model=MODEL_GEMINI_1_5_FLASH,  # Using Gemini 1.5 Flash
            description="Provides weather information (using Gemini 1.5 Flash).",
            instruction="You are a helpful weather assistant powered by Gemini 1.5 Flash. "
                        "Use the 'get_weather' tool for city weather requests. "
                        "Analyze the tool's dictionary output ('status', 'report'/'error_message'). "
                        "Clearly present successful reports or polite error messages.",
            tools=[get_weather],  # Re-use the same tool
        )
        print(f"Agent '{weather_agent_gemini_flash.name}' created using model '{MODEL_GEMINI_1_5_FLASH}'.")

        # InMemorySessionService is simple, non-persistent storage for this tutorial.
        session_service_gemini_flash = InMemorySessionService()  # Create a dedicated service

        # Define constants for identifying the interaction context
        APP_NAME_GEMINI_FLASH = "weather_tutorial_app_gemini_flash"  # Unique app name
        USER_ID_GEMINI_FLASH = "user_1_gemini_flash"
        SESSION_ID_GEMINI_FLASH = "session_001_gemini_flash"  # Using a fixed ID for simplicity

        # Create the specific session where the conversation will happen
        session_gemini_flash = await session_service_gemini_flash.create_session(
            app_name=APP_NAME_GEMINI_FLASH,
            user_id=USER_ID_GEMINI_FLASH,
            session_id=SESSION_ID_GEMINI_FLASH
        )
        print(f"Session created: App='{APP_NAME_GEMINI_FLASH}', User='{USER_ID_GEMINI_FLASH}', Session='{SESSION_ID_GEMINI_FLASH}'")

        # Create a runner specific to this agent and its session service
        runner_gemini_flash = Runner(
            agent=weather_agent_gemini_flash,
            app_name=APP_NAME_GEMINI_FLASH,       # Use the specific app name
            session_service=session_service_gemini_flash  # Use the specific session service
        )
        print(f"Runner created for agent '{runner_gemini_flash.agent.name}'.")

        # --- Test the Gemini Flash Agent ---
        print("\n--- Testing Gemini 1.5 Flash Agent ---")
        # Ensure call_agent_async uses the correct runner, user_id, session_id
        await call_agent_async(query="Weather in London please.",
                               runner=runner_gemini_flash,
                               user_id=USER_ID_GEMINI_FLASH,
                               session_id=SESSION_ID_GEMINI_FLASH)

    except Exception as e:
        print(f"❌ Could not create or run Gemini Flash agent '{MODEL_GEMINI_1_5_FLASH}'. Error: {e}")

# Test original agent (Gemini)
if __name__ == "__main__":
    asyncio.run(run_conversation())

# Test Gemini Pro agent
if __name__ == "__main__":
    asyncio.run(test_gemini_pro_agent())

# Test Gemini Flash agent
if __name__ == "__main__":
    asyncio.run(test_gemini_flash_agent())