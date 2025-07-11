# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Zoom Support Agent Runner: Main orchestration for customer service requests."""

import asyncio
import sys
import os
from google.adk.runners import InMemoryRunner
from google.genai import types

# Handle imports for both direct execution and module import
try:
    from .agent import root_agent
except ImportError:
    # When running as script, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from zoom_support_agent.agent import root_agent

async def run_zoom_support_query(user_query: str, customer_email: str = None) -> str:
    """
    Run a customer service query through the Zoom support agent system.
    
    Args:
        user_query (str): The customer's question or request
        customer_email (str, optional): Customer's email for purchase verification
        
    Returns:
        str: The agent's response to the customer
    """
    print(f"\n=== Zoom Support Agent Query ===")
    print(f"Customer Query: {user_query}")
    if customer_email:
        print(f"Customer Email: {customer_email}")
    print("=" * 40)
    
    # Create the runner with the root agent
    runner = InMemoryRunner(agent=root_agent)
    
    try:
        # Create a session first using the runner's session service
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="customer",
            session_id="zoom_support_session"
        )
        
        # Create a simple user message
        user_message = types.Content(parts=[types.Part(text=user_query)])
        
        # Run the query through the agent system
        events = []
        async for event in runner.run_async(
            user_id="customer",
            session_id="zoom_support_session",
            new_message=user_message
        ):
            events.append(event)
            # Print intermediate events for debugging
            if hasattr(event, 'content') and event.content:
                print(f"Event: {event.content}")
        
        # Extract the final response from the last event
        final_response = ""
        for event in reversed(events):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text
                            break
                if final_response:
                    break
        
        print(f"\n=== Agent Response ===")
        print(final_response)
        print("=" * 40)
        
        return final_response
        
    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        print(f"\n=== Error ===")
        print(error_message)
        print("=" * 40)
        return error_message
    finally:
        await runner.close()

async def main():
    """Main function to demonstrate the Zoom support agent system."""
    
    # Sample customer query
    sample_query = "I just bought a Zoom H6 but I'm not sure how to register it or find compatible mics"
    customer_email = "john.doe@email.com"
    
    print("🎤 Zoom Support Agent System")
    print("=" * 50)
    print("This system coordinates between specialized agents to provide comprehensive customer support.")
    print("Agents available:")
    print("- Product Search: Identifies Zoom products and provides specifications")
    print("- Third-party Web Search: Finds compatible gear and accessories") 
    print("- Customer Specialist: Handles warranty, registration, and purchase verification")
    print("=" * 50)
    
    # Run the sample query
    response = await run_zoom_support_query(sample_query, customer_email)
    
    print(f"\n🎯 Final Response:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main()) 