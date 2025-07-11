#!/usr/bin/env python3
"""
Zoom Support Agent Launcher
Simple launcher script to run the Zoom support agent system.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zoom_support_agent.runner import run_zoom_support_query

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